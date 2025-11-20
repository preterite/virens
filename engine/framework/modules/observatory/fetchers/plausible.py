#!/usr/bin/env python3
"""
Plausible Analytics API fetcher (PLACEHOLDER)
Website analytics for preterition.net
Will be activated after Jekyll migration
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "AcademicSync/SRE"))

from observatory.core.config import config
from observatory.core.database import db
from observatory.fetchers.base import BaseFetcher

class PlausibleFetcher(BaseFetcher):
    """Fetch data from Plausible Analytics API (PLACEHOLDER)"""
    
    def __init__(self):
        super().__init__("plausible", rate_limit_delay=1.0)
        self.site_id = config.credentials.get("plausible", {}).get("site_id", "preterition.net")
        self.api_key = config.credentials.get("plausible", {}).get("api_key")
        self.enabled = config.is_service_enabled("plausible")
        self.base_url = "https://plausible.io/api/v1"
        
        if not self.enabled:
            self._log("Plausible integration is disabled (awaiting Jekyll migration)", "INFO")
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with authentication and caching"""
        if not self.enabled or not self.api_key:
            self._log("Plausible not configured - skipping request", "INFO")
            return None
        
        url = f"{self.base_url}/{endpoint}"
        
        # Check cache first
        cache_key = self._cache_key(url, params)
        cached = self._read_cache(cache_key, max_age_hours=24)
        if cached:
            self._log(f"Using cached data for {endpoint}")
            return cached
        
        # Rate limit
        self._rate_limit()
        
        # Setup headers
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
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
    
    def get_aggregate_stats(self, period: str = "30d") -> Optional[Dict]:
        """
        Get aggregate statistics for the site
        
        Args:
            period: Time period (e.g., "30d", "7d", "month", "12mo")
        """
        if not self.enabled:
            return self._placeholder_data()
        
        params = {
            "site_id": self.site_id,
            "period": period,
            "metrics": "visitors,pageviews,bounce_rate,visit_duration"
        }
        
        return self._make_request(f"stats/aggregate", params)
    
    def get_timeseries(self, period: str = "30d") -> Optional[Dict]:
        """Get time-series data for visitors"""
        if not self.enabled:
            return self._placeholder_data()
        
        params = {
            "site_id": self.site_id,
            "period": period,
            "metrics": "visitors,pageviews"
        }
        
        return self._make_request(f"stats/timeseries", params)
    
    def get_top_pages(self, period: str = "30d", limit: int = 10) -> Optional[Dict]:
        """Get most visited pages"""
        if not self.enabled:
            return self._placeholder_data()
        
        params = {
            "site_id": self.site_id,
            "period": period,
            "limit": limit
        }
        
        return self._make_request(f"stats/breakdown", params)
    
    def _placeholder_data(self) -> Dict:
        """Return placeholder data when Plausible is not enabled"""
        return {
            "status": "placeholder",
            "message": "Plausible analytics will be available after Jekyll migration",
            "site_id": self.site_id,
            "enabled": False
        }
    
    def update_metrics(self):
        """Update website analytics metrics in database"""
        if not self.enabled:
            self._log("Plausible is disabled - storing placeholder", "INFO")
            
            timestamp = datetime.now().isoformat()
            
            # Store placeholder metric
            db.add_external_metric(
                source="plausible",
                metric_name="status",
                metric_value="placeholder",
                metadata={
                    "message": "Awaiting Jekyll migration and Plausible setup",
                    "site_id": self.site_id
                },
                fetched_at=timestamp
            )
            
            self._log("Placeholder metric stored - activate after Jekyll migration")
            return
        
        # When enabled, fetch real data
        timestamp = datetime.now().isoformat()
        
        # Get 30-day aggregate stats
        stats = self.get_aggregate_stats(period="30d")
        
        if stats and "status" not in stats:
            # Store visitor count
            if "visitors" in stats.get("results", {}):
                db.add_external_metric(
                    source="plausible",
                    metric_name="visitors_30d",
                    metric_value=str(stats["results"]["visitors"]["value"]),
                    metadata=None,
                    fetched_at=timestamp
                )
            
            # Store pageviews
            if "pageviews" in stats.get("results", {}):
                db.add_external_metric(
                    source="plausible",
                    metric_name="pageviews_30d",
                    metric_value=str(stats["results"]["pageviews"]["value"]),
                    metadata=None,
                    fetched_at=timestamp
                )
            
            # Store bounce rate
            if "bounce_rate" in stats.get("results", {}):
                db.add_external_metric(
                    source="plausible",
                    metric_name="bounce_rate",
                    metric_value=str(stats["results"]["bounce_rate"]["value"]),
                    metadata=None,
                    fetched_at=timestamp
                )
            
            self._log(f"Updated Plausible metrics for {self.site_id}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of website analytics for display"""
        if not self.enabled:
            return {
                "enabled": False,
                "message": "Plausible analytics will be available after Jekyll migration",
                "site_id": self.site_id
            }
        
        # Get recent metrics from database
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT metric_name, metric_value, metadata
                FROM external_metrics
                WHERE source = 'plausible'
                AND id IN (
                    SELECT MAX(id)
                    FROM external_metrics
                    WHERE source = 'plausible'
                    GROUP BY metric_name
                )
            ''')
            
            metrics = {}
            for row in cursor.fetchall():
                metrics[row['metric_name']] = {
                    'value': row['metric_value'],
                    'metadata': row['metadata']
                }
        
        return {
            "enabled": True,
            "site_id": self.site_id,
            "metrics": metrics
        }

def fetch_plausible_data():
    """Convenience function to fetch Plausible analytics data"""
    fetcher = PlausibleFetcher()
    fetcher.update_metrics()

if __name__ == "__main__":
    fetch_plausible_data()
