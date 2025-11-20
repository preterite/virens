#!/usr/bin/env python3
"""
OpenAlex API fetcher
Comprehensive publication metadata
Free and open API
"""
import requests
from typing import Dict, List, Optional, Any
import yaml
from pathlib import Path

# Load user configuration
def get_user_config():
    """Load user configuration from user instance"""
    virens_file = Path.home() / '.virens'
    if virens_file.exists():
        user_dir = Path(virens_file.read_text().strip())
        config_file = user_dir / 'config' / 'observatory.yaml'
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
    return {}

# Load user config at module level
_user_config = get_user_config()
USER_EMAIL = _user_config.get('user', {}).get('email', 'user@example.edu')
USER_NAME = _user_config.get('user', {}).get('name', 'Research User')

# Import observatory modules (no sys.path hack needed in new structure)
from observatory.core.config import config
from observatory.core.database import db
from observatory.fetchers.base import BaseFetcher


class OpenAlexFetcher(BaseFetcher):
    """Fetch data from OpenAlex API"""
    
    def __init__(self):
        super().__init__("openalex", rate_limit_delay=0.1)
        self.base_url = "https://api.openalex.org"
        # OpenAlex asks for email for polite usage (from user config)
        self.email = USER_EMAIL
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with caching and rate limiting"""
        url = f"{self.base_url}/{endpoint}"
        
        # Add email to params for polite pool
        if params is None:
            params = {}
        params["mailto"] = self.email
        
        # Check cache first
        cache_key = self._cache_key(url, params)
        cached = self._read_cache(cache_key, max_age_hours=24)
        if cached:
            self._log(f"Using cached data for {endpoint}")
            return cached
        
        # Rate limit
        self._rate_limit()
        
        try:
            self._log(f"Fetching: {endpoint}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the response
            self._write_cache(cache_key, data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            self._log(f"Request failed: {e}", "ERROR")
            return None
    
    def search_author(self, author_name: str) -> Optional[str]:
        """Search for author by name, return OpenAlex author ID"""
        # OpenAlex uses display_name for searching
        params = {
            "search": author_name,
            "per-page": 5
        }
        
        data = self._make_request("authors", params)
        
        if data and "results" in data and len(data["results"]) > 0:
            # Look for best match
            for author in data["results"]:
                display_name = author.get("display_name", "")
                # Simple matching - could be improved
                if "edwards" in display_name.lower() and "mike" in display_name.lower():
                    author_id = author["id"]
                    self._log(f"Found author: {display_name} ({author_id})")
                    return author_id
            
            # Return first if no perfect match
            first = data["results"][0]
            self._log(f"Using closest match: {first['display_name']}")
            return first["id"]
        
        return None
    
    def get_author_works(self, author_id: str) -> List[Dict]:
        """Get all works for an author"""
        # Extract the OpenAlex ID part (after the URL)
        if author_id.startswith("https://openalex.org/"):
            author_id = author_id.replace("https://openalex.org/", "")
        
        params = {
            "filter": f"author.id:{author_id}",
            "per-page": 100
        }
        
        data = self._make_request("works", params)
        
        if data and "results" in data:
            works = data["results"]
            self._log(f"Found {len(works)} works")
            return works
        
        return []
    
    def search_work_by_title(self, title: str, year: Optional[int] = None) -> Optional[Dict]:
        """Search for a specific work by title and optionally year"""
        # Clean title for better matching
        search_title = title.replace(":", "").replace("?", "")
        
        params = {
            "search": search_title,
            "per-page": 10
        }
        
        # Add year filter if provided
        if year:
            params["filter"] = f"publication_year:{year}"
        
        data = self._make_request("works", params)
        
        if data and "results" in data:
            results = data["results"]
            
            # Try to find exact or close match
            for work in results:
                work_title = work.get("title", "").lower()
                search_lower = title.lower()
                
                # Check for substantial overlap
                if self._title_similarity(work_title, search_lower) > 0.7:
                    return work
            
            # If no good match and we have results, return first
            if results:
                self._log(f"Using best available match for: {title[:40]}...", "WARN")
                return results[0]
        
        return None
    
    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate simple similarity score between titles"""
        # Remove common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        
        words1 = set(title1.lower().split()) - stop_words
        words2 = set(title2.lower().split()) - stop_words
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def enrich_publication(self, pub_id: int, pub_data: Dict) -> bool:
        """Enrich a publication record with OpenAlex data"""
        title = pub_data["title"]
        year = pub_data.get("year")
        
        # Search for the work
        work = self.search_work_by_title(title, year)
        
        if not work:
            self._log(f"Could not find work: {title[:50]}...", "WARN")
            return False
        
        # Update publication with OpenAlex ID
        work_id = work["id"].replace("https://openalex.org/", "")
        pub_data["openalex_id"] = work_id
        
        # Get DOI if we don't have it
        if not pub_data.get("doi"):
            doi = work.get("doi")
            if doi:
                # Strip the https://doi.org/ prefix if present
                pub_data["doi"] = doi.replace("https://doi.org/", "")
        
        # Get abstract if we don't have it
        if not pub_data.get("abstract"):
            inverted_abstract = work.get("abstract_inverted_index")
            if inverted_abstract:
                # Reconstruct abstract from inverted index
                pub_data["abstract"] = self._reconstruct_abstract(inverted_abstract)
        
        # Save updated publication
        db.add_publication(pub_data)
        
        # Record citation count
        citation_count = work.get("cited_by_count", 0)
        db.add_citation_count(pub_id, citation_count, "openalex")
        
        self._log(f"Enriched: {title[:50]}... ({citation_count} citations)")
        
        return True
    
    def _reconstruct_abstract(self, inverted_index: Dict[str, List[int]]) -> str:
        """Reconstruct abstract text from OpenAlex inverted index"""
        if not inverted_index:
            return ""
        
        # Build list of (position, word) tuples
        words = []
        for word, positions in inverted_index.items():
            for pos in positions:
                words.append((pos, word))
        
        # Sort by position and join
        words.sort()
        abstract = " ".join(word for _, word in words)
        
        # Truncate if very long
        if len(abstract) > 2000:
            abstract = abstract[:2000] + "..."
        
        return abstract
    
    def update_all_citations(self):
        """Update citation counts for all publications in database"""
        pubs = db.get_publications()
        
        self._log(f"Updating citations for {len(pubs)} publications...")
        
        updated = 0
        for pub in pubs:
            if self.enrich_publication(pub["id"], pub):
                updated += 1
        
        self._log(f"Updated {updated}/{len(pubs)} publications")
        
        # Calculate and store h-index
        self._calculate_h_index()
    
    def _calculate_h_index(self):
        """Calculate h-index from OpenAlex citation data"""
        # Get all publications with OpenAlex IDs
        pubs = db.get_publications()
        openalex_pubs = [p for p in pubs if p.get("openalex_id")]
        
        if not openalex_pubs:
            self._log("No publications with OpenAlex data", "WARN")
            return
        
        # Get latest citation count for each
        citation_counts = []
        for pub in openalex_pubs:
            history = db.get_citation_history(pub["id"])
            if history:
                # Get most recent OpenAlex citation count
                openalex_cites = [h for h in history if h["source"] == "openalex"]
                if openalex_cites:
                    citation_counts.append(openalex_cites[-1]["citation_count"])
        
        if not citation_counts:
            self._log("No citation data available", "WARN")
            return
        
        # Sort descending
        citation_counts.sort(reverse=True)
        
        # Calculate h-index
        h_index = 0
        for i, citations in enumerate(citation_counts, 1):
            if citations >= i:
                h_index = i
            else:
                break
        
        # Store metrics
        db.add_metric("h_index_openalex", float(h_index), {"source": "openalex"})
        
        total_citations = sum(citation_counts)
        db.add_metric("total_citations_openalex", float(total_citations), {"source": "openalex"})
        
        i10_index = sum(1 for c in citation_counts if c >= 10)
        db.add_metric("i10_index_openalex", float(i10_index), {"source": "openalex"})
        
        self._log(f"OpenAlex metrics: h-index={h_index}, total={total_citations}, i10={i10_index}")
    
    def find_similar_researchers(self, limit: int = 20) -> List[Dict]:
        """Find researchers with similar publication patterns (for peer comparison)"""
        # Get your publications
        pubs = db.get_publications()
        openalex_pubs = [p for p in pubs if p.get("openalex_id")]
        
        if not openalex_pubs:
            return []
        
        # Get concepts from your papers
        concepts = set()
        for pub in openalex_pubs[:5]:  # Use top 5 papers
            work_id = pub["openalex_id"]
            if not work_id.startswith("W"):
                work_id = "W" + work_id
            
            data = self._make_request(f"works/{work_id}", {})
            if data and "concepts" in data:
                for concept in data["concepts"]:
                    if concept.get("score", 0) > 0.3:  # Significant concepts only
                        concepts.add(concept["id"])
        
        # Search for authors with similar concepts
        # This is a simplified version - could be more sophisticated
        self._log(f"Found {len(concepts)} key concepts, searching for similar researchers...")
        
        return []  # Placeholder for now

def fetch_openalex_data():
    """Convenience function to fetch all OpenAlex data"""
    fetcher = OpenAlexFetcher()
    fetcher.update_all_citations()

if __name__ == "__main__":
    fetch_openalex_data()
