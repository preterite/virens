#!/usr/bin/env python3
"""
Semantic Scholar API fetcher
Gets citation data, author information, and paper metadata
"""

import requests
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "AcademicSync/SRE"))

from observatory.core.config import config
from observatory.core.database import db
from observatory.fetchers.base import BaseFetcher

class SemanticScholarFetcher(BaseFetcher):
    """Fetch data from Semantic Scholar API"""
    
    def __init__(self):
        super().__init__("semantic_scholar", rate_limit_delay=1.0)
        self.api_key = config.get_api_key("semantic_scholar")
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        
        if not self.api_key:
            self._log("WARNING: No API key found, using public API (lower rate limits)", "WARN")
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with caching and rate limiting"""
        url = f"{self.base_url}/{endpoint}"
        
        # Check cache first
        cache_key = self._cache_key(url, params)
        cached = self._read_cache(cache_key, max_age_hours=24)
        if cached:
            self._log(f"Using cached data for {endpoint}")
            return cached
        
        # Rate limit
        self._rate_limit()
        
        # Make request
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        
        try:
            self._log(f"Fetching: {endpoint}")
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the response
            self._write_cache(cache_key, data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            self._log(f"Request failed: {e}", "ERROR")
            return None
    
    def search_author(self, author_name: str) -> Optional[str]:
        """Search for author by name, return author ID"""
        params = {
            "query": author_name,
            "fields": "authorId,name,paperCount,citationCount,hIndex"
        }
        
        data = self._make_request("author/search", params)
        
        if data and "data" in data and len(data["data"]) > 0:
            # Return first match (usually correct for unique names)
            author = data["data"][0]
            self._log(f"Found author: {author['name']} (ID: {author['authorId']})")
            return author["authorId"]
        
        return None
    
    def get_author_papers(self, author_id: str) -> List[Dict]:
        """Get all papers for an author"""
        params = {
            "fields": "paperId,title,year,authors,venue,citationCount,abstract,externalIds",
            "limit": 100
        }
        
        data = self._make_request(f"author/{author_id}/papers", params)
        
        if data and "data" in data:
            papers = data["data"]
            self._log(f"Found {len(papers)} papers")
            return papers
        
        return []
    
    def get_paper_by_title(self, title: str) -> Optional[Dict]:
        """Search for a specific paper by title"""
        params = {
            "query": title,
            "fields": "paperId,title,year,authors,venue,citationCount,abstract,externalIds",
            "limit": 1
        }
        
        data = self._make_request("paper/search", params)
        
        if data and "data" in data and len(data["data"]) > 0:
            return data["data"][0]
        
        return None
    
    def enrich_publication(self, pub_id: int, pub_data: Dict) -> bool:
        """Enrich a publication record with Semantic Scholar data"""
        title = pub_data["title"]
        
        # Search for the paper
        paper = self.get_paper_by_title(title)
        
        if not paper:
            self._log(f"Could not find paper: {title[:50]}...", "WARN")
            return False
        
        # Update publication with Semantic Scholar ID
        pub_data["semantic_scholar_id"] = paper["paperId"]
        
        # Extract OpenAlex ID if available
        external_ids = paper.get("externalIds", {})
        if "OpenAlex" in external_ids:
            pub_data["openalex_id"] = external_ids["OpenAlex"]
        
        # Update DOI if we don't have it
        if not pub_data.get("doi") and "DOI" in external_ids:
            pub_data["doi"] = external_ids["DOI"]
        
        # Update abstract if we don't have it
        if not pub_data.get("abstract") and paper.get("abstract"):
            pub_data["abstract"] = paper["abstract"]
        
        # Save updated publication
        db.add_publication(pub_data)
        
        # Record citation count
        citation_count = paper.get("citationCount", 0)
        db.add_citation_count(pub_id, citation_count, "semantic_scholar")
        
        self._log(f"Enriched: {title[:50]}... ({citation_count} citations)")
        
        return True
    
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
        """Calculate h-index from citation data"""
        # Get latest citations for all papers
        citations = db.get_latest_citations()
        
        # Extract just the citation counts and sort descending
        citation_counts = sorted([c[2] for c in citations], reverse=True)
        
        # Calculate h-index
        h_index = 0
        for i, citations in enumerate(citation_counts, 1):
            if citations >= i:
                h_index = i
            else:
                break
        
        # Store h-index
        db.add_metric("h_index", float(h_index), {"source": "semantic_scholar"})
        
        # Calculate total citations
        total_citations = sum(citation_counts)
        db.add_metric("total_citations", float(total_citations), {"source": "semantic_scholar"})
        
        # Calculate i10-index (papers with 10+ citations)
        i10_index = sum(1 for c in citation_counts if c >= 10)
        db.add_metric("i10_index", float(i10_index), {"source": "semantic_scholar"})
        
        self._log(f"Calculated metrics: h-index={h_index}, total citations={total_citations}, i10={i10_index}")

def fetch_semantic_scholar_data():
    """Convenience function to fetch all Semantic Scholar data"""
    fetcher = SemanticScholarFetcher()
    fetcher.update_all_citations()

if __name__ == "__main__":
    fetch_semantic_scholar_data()
