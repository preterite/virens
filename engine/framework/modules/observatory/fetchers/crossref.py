#!/usr/bin/env python3
"""
CrossRef API fetcher
DOI resolution and journal metadata
Free API using polite pool
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


class CrossRefFetcher(BaseFetcher):
    """Fetch data from CrossRef API"""
    
    def __init__(self):
        super().__init__("crossref", rate_limit_delay=0.5)
        self.base_url = "https://api.crossref.org"
        # Use email for polite pool (from user config)
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
        cached = self._read_cache(cache_key, max_age_hours=168)  # Cache for 1 week
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
    
    def get_work_by_doi(self, doi: str) -> Optional[Dict]:
        """Get work metadata by DOI"""
        # Clean DOI
        doi = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
        
        data = self._make_request(f"works/{doi}", {})
        
        if data and "message" in data:
            return data["message"]
        
        return None
    
    def search_by_title(self, title: str, author: Optional[str] = None) -> Optional[Dict]:
        """Search for work by title and optionally author"""
        params = {
            "query.title": title,
            "rows": 5
        }
        
        if author:
            # Extract last name for better matching
            author_parts = author.split()
            last_name = author_parts[-1] if author_parts else author
            params["query.author"] = last_name
        
        data = self._make_request("works", params)
        
        if data and "message" in data and "items" in data["message"]:
            items = data["message"]["items"]
            
            if not items:
                return None
            
            # Find best match by title similarity
            best_match = None
            best_score = 0
            
            for item in items:
                item_title = item.get("title", [""])[0].lower()
                search_title = title.lower()
                
                score = self._title_similarity(item_title, search_title)
                
                if score > best_score:
                    best_score = score
                    best_match = item
            
            # Only return if we have a decent match
            if best_score > 0.6:
                return best_match
        
        return None
    
    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate simple similarity score between titles"""
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of"}
        
        words1 = set(title1.lower().split()) - stop_words
        words2 = set(title2.lower().split()) - stop_words
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def enrich_publication(self, pub_id: int, pub_data: Dict) -> bool:
        """Enrich a publication record with CrossRef data"""
        work = None
        
        # Try DOI lookup first if we have one
        if pub_data.get("doi"):
            work = self.get_work_by_doi(pub_data["doi"])
        
        # Fall back to title search
        if not work:
            title = pub_data["title"]
            author = pub_data.get("authors", "").split(",")[0] if pub_data.get("authors") else None
            work = self.search_by_title(title, author)
        
        if not work:
            self._log(f"Could not find work: {pub_data['title'][:50]}...", "WARN")
            return False
        
        # Update DOI if we don't have it
        if not pub_data.get("doi") and work.get("DOI"):
            pub_data["doi"] = work["DOI"]
        
        # Update venue/journal information
        if not pub_data.get("venue") and work.get("container-title"):
            container = work["container-title"]
            if container and len(container) > 0:
                pub_data["venue"] = container[0]
        
        # Update year if missing
        if not pub_data.get("year") and work.get("published-print"):
            date_parts = work["published-print"].get("date-parts", [[]])
            if date_parts and len(date_parts[0]) > 0:
                pub_data["year"] = date_parts[0][0]
        
        # Update abstract if missing
        if not pub_data.get("abstract") and work.get("abstract"):
            pub_data["abstract"] = work["abstract"]
        
        # Extract ISSN for journal tracking
        metadata = {
            "issn": work.get("ISSN", []),
            "publisher": work.get("publisher"),
            "type": work.get("type"),
            "is_referenced_by_count": work.get("is-referenced-by-count", 0)
        }
        
        # Save updated publication
        db.add_publication(pub_data)
        
        # Record citation count if available
        if work.get("is-referenced-by-count"):
            db.add_citation_count(pub_id, work["is-referenced-by-count"], "crossref")
        
        self._log(f"Enriched: {pub_data['title'][:50]}... (DOI: {pub_data.get('doi', 'N/A')})")
        
        return True
    
    def update_all_metadata(self):
        """Update metadata for all publications in database"""
        pubs = db.get_publications()
        
        self._log(f"Updating metadata for {len(pubs)} publications...")
        
        updated = 0
        for pub in pubs:
            if self.enrich_publication(pub["id"], pub):
                updated += 1
        
        self._log(f"Updated {updated}/{len(pubs)} publications")
    
    def get_journal_metadata(self, issn: str) -> Optional[Dict]:
        """Get journal metadata by ISSN"""
        data = self._make_request(f"journals/{issn}", {})
        
        if data and "message" in data:
            return data["message"]
        
        return None
    
    def check_monitored_journals(self) -> List[Dict]:
        """Check for recent publications in monitored journals"""
        journals = config.journals["journals"]
        
        self._log(f"Checking {len(journals)} monitored journals...")
        
        recent_papers = []
        
        for journal in journals:
            issn = journal.get("issn")
            if not issn:
                continue
            
            # Search for recent papers in this journal
            params = {
                "filter": f"issn:{issn}",
                "sort": "published",
                "order": "desc",
                "rows": 10  # Get 10 most recent
            }
            
            data = self._make_request("works", params)
            
            if data and "message" in data and "items" in data["message"]:
                items = data["message"]["items"]
                
                for item in items:
                    # Check if paper matches your research interests
                    title = item.get("title", [""])[0]
                    abstract = item.get("abstract", "")
                    
                    # Simple keyword matching
                    text = f"{title} {abstract}".lower()
                    
                    keywords = config.fields.get("keywords", [])
                    matches = sum(1 for kw in keywords if kw.lower() in text)
                    
                    if matches >= 2:  # At least 2 keyword matches
                        recent_papers.append({
                            "title": title,
                            "journal": journal["title"],
                            "doi": item.get("DOI"),
                            "published": item.get("published-print", {}),
                            "relevance_keywords": matches
                        })
        
        self._log(f"Found {len(recent_papers)} potentially relevant papers")
        
        return recent_papers

def fetch_crossref_data():
    """Convenience function to fetch all CrossRef data"""
    fetcher = CrossRefFetcher()
    fetcher.update_all_metadata()

if __name__ == "__main__":
    fetch_crossref_data()
