#!/usr/bin/env python3
"""
OpenAlex API fetcher
Comprehensive publication metadata
Free and open API
"""
import json
import requests
from datetime import datetime
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
ORCID_ID = _user_config.get('researcher', {}).get('orcid_id', '')

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
    
    def get_works_by_orcid(self, orcid_id: str) -> List[Dict]:
        """Get all works for a researcher by ORCID ID"""
        params = {
            "filter": f"author.orcid:{orcid_id}",
            "per-page": 200
        }

        data = self._make_request("works", params)

        if data and "results" in data:
            works = data["results"]
            self._log(f"Found {len(works)} works for ORCID {orcid_id}")
            return works

        return []

    def _find_work_in_results(self, title: str, works: List[Dict], year: Optional[int] = None) -> Optional[Dict]:
        """Find a specific work by title (and optionally year) within a list of works"""
        best_match = None
        best_score = 0.0

        for work in works:
            work_title = work.get("title", "")
            if not work_title:
                continue

            # Year filter if provided
            if year and work.get("publication_year") != year:
                continue

            score = self._title_similarity(work_title.lower(), title.lower())
            if score > best_score:
                best_score = score
                best_match = work

        if best_match and best_score > 0.5:
            self._log(f"ORCID match (score {best_score:.2f}): {best_match.get('title', '')[:60]}...")
            return best_match

        return None

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
    
    def get_work_by_doi(self, doi: str) -> Optional[Dict]:
        """Look up a work directly by DOI — most reliable identification method."""
        # Normalise DOI: strip https://doi.org/ prefix if present
        doi_clean = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
        data = self._make_request(f"works/https://doi.org/{doi_clean}", {})
        if data and "id" in data:
            self._log(f"DOI lookup succeeded: {doi_clean}")
            return data
        self._log(f"DOI lookup returned no result: {doi_clean}", "WARN")
        return None

    def enrich_publication(self, pub_id: int, pub_data: Dict) -> bool:
        """Enrich a publication record with OpenAlex data.

        Strategy (in priority order):
        1. DOI lookup — direct, unambiguous, no name-disambiguation risk.
        2. ORCID-filtered title match — if DOI absent and ORCID is indexed.
        3. Generic title search — last resort, prone to false matches; logged as WARN.
        """
        title = pub_data["title"]
        year = pub_data.get("year")
        doi = pub_data.get("doi")

        work = None

        # Strategy 1: DOI lookup (preferred)
        if doi:
            work = self.get_work_by_doi(doi)

        # Strategy 2: ORCID-filtered title match
        if not work and ORCID_ID:
            if not hasattr(self, '_orcid_works_cache'):
                self._orcid_works_cache = self.get_works_by_orcid(ORCID_ID)
            if self._orcid_works_cache:
                work = self._find_work_in_results(title, self._orcid_works_cache, year)

        # Strategy 3: generic title search (last resort)
        if not work:
            self._log(f"DOI/ORCID lookup miss, falling back to title search: {title[:50]}...", "WARN")
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
        
        # Get authors from OpenAlex if we don't have them
        if not pub_data.get("authors"):
            authorships = work.get("authorships", [])
            author_names = [
                a.get("author", {}).get("display_name", "")
                for a in authorships
                if a.get("author", {}).get("display_name")
            ]
            if author_names:
                pub_data["authors"] = ", ".join(author_names)

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

    def fetch_field_papers(self, days_back: int = 90, relevance_threshold: int = 2) -> List[Dict]:
        """
        Fetch recent papers from monitored journals via OpenAlex.
        Scores each paper against monitored keywords; stores papers meeting threshold.
        """
        from datetime import date, timedelta
        import json as _json

        # Load journals and keywords from user config
        journals = _user_config.get('monitored_journals', [])
        keywords = _user_config.get('trend_keywords', [])

        if not journals:
            self._log("No journals configured in observatory.yaml — skipping field papers fetch", "WARN")
            return []

        if not keywords:
            self._log("No keywords configured in observatory.yaml — scoring disabled", "WARN")

        since_date = (date.today() - timedelta(days=days_back)).isoformat()
        all_papers = []

        for journal in journals:
            issn = journal.get('issn')
            name = journal.get('name', issn)

            if not issn:
                self._log(f"Journal entry missing ISSN, skipping: {journal}", "WARN")
                continue

            self._log(f"Fetching recent papers from {name} (ISSN {issn}) since {since_date}")

            params = {
                "filter": f"primary_location.source.issn:{issn},from_publication_date:{since_date}",
                "per-page": 50,
                "select": "id,title,publication_year,publication_date,cited_by_count,concepts,abstract_inverted_index,authorships,primary_location"
            }

            data = self._make_request("works", params)

            if not data or "results" not in data:
                self._log(f"No results for {name}", "WARN")
                continue

            for work in data["results"]:
                title = work.get("title", "")
                if not title:
                    continue

                # Score against keywords
                score = self._score_paper_relevance(work, keywords)

                if score < relevance_threshold:
                    continue

                # Reconstruct abstract if available
                abstract = ""
                inv_abstract = work.get("abstract_inverted_index")
                if inv_abstract:
                    abstract = self._reconstruct_abstract(inv_abstract)

                # Build author list
                authorships = work.get("authorships", [])
                authors = [
                    a.get("author", {}).get("display_name", "")
                    for a in authorships
                    if a.get("author", {}).get("display_name")
                ]

                paper = {
                    "openalex_id": work["id"].replace("https://openalex.org/", ""),
                    "title": title,
                    "journal": name,
                    "issn": issn,
                    "year": work.get("publication_year"),
                    "publication_date": work.get("publication_date"),
                    "citation_count": work.get("cited_by_count", 0),
                    "abstract": abstract,
                    "authors": authors,
                    "relevance_score": score,
                    "matched_keywords": self._get_matched_keywords(work, keywords),
                    "fetched_at": datetime.now().isoformat()
                }

                all_papers.append(paper)
                self._log(f"  Scored {score}: {title[:60]}...")

        self._log(f"fetch_field_papers: {len(all_papers)} relevant papers across all journals")

        # Write to raw JSON for TrendAnalyzer
        raw_dir = config.observatory_data / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        field_papers_path = raw_dir / "field_papers.json"
        field_papers_path.write_text(_json.dumps(all_papers, indent=2))
        self._log(f"Written: {field_papers_path}")

        # Store in database
        for paper in all_papers:
            db.add_field_paper(paper)

        return all_papers

    def _score_paper_relevance(self, work: Dict, keywords: List[str]) -> int:
        """Count how many monitored keywords appear in title, abstract, or concepts."""
        if not keywords:
            return 0

        title = (work.get("title") or "").lower()

        abstract_text = ""
        inv_abstract = work.get("abstract_inverted_index")
        if inv_abstract:
            abstract_text = " ".join(inv_abstract.keys()).lower()

        concept_names = [
            c.get("display_name", "").lower()
            for c in work.get("concepts", [])
            if c.get("score", 0) > 0.3
        ]
        concept_text = " ".join(concept_names)

        full_text = f"{title} {abstract_text} {concept_text}"

        return sum(1 for kw in keywords if kw.lower() in full_text)

    def _get_matched_keywords(self, work: Dict, keywords: List[str]) -> List[str]:
        """Return list of keywords that matched this paper."""
        if not keywords:
            return []

        title = (work.get("title") or "").lower()
        abstract_text = ""
        inv_abstract = work.get("abstract_inverted_index")
        if inv_abstract:
            abstract_text = " ".join(inv_abstract.keys()).lower()
        concept_names = [
            c.get("display_name", "").lower()
            for c in work.get("concepts", [])
            if c.get("score", 0) > 0.3
        ]
        full_text = f"{title} {abstract_text} {' '.join(concept_names)}"

        return [kw for kw in keywords if kw.lower() in full_text]


def fetch_openalex_data():
    """Convenience function to fetch all OpenAlex data"""
    fetcher = OpenAlexFetcher()
    fetcher.update_all_citations()


def fetch_field_papers_data(mode: str = "recent") -> list:
    """Convenience function to fetch field papers.

    Args:
        mode: "recent" (default) — 90 days, feeds weekly reporter.
              "annual"           — 365 days, feeds TrendAnalyzer monthly run.
    """
    if mode not in ("recent", "annual"):
        raise ValueError(f"mode must be 'recent' or 'annual', got '{mode}'")
    days = 365 if mode == "annual" else 90
    fetcher = OpenAlexFetcher()
    return fetcher.fetch_field_papers(days_back=days)


if __name__ == "__main__":
    fetch_openalex_data()
