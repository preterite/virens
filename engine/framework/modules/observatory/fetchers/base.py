#!/usr/bin/env python3
"""
Base fetcher class with common functionality
Handles rate limiting, caching, and error handling
"""

import time
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class BaseFetcher:
    """Base class for API fetchers"""
    
    def __init__(self, name: str, rate_limit_delay: float = 1.0):
        self.name = name
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        self.cache_dir = Path.home() / "Local/virens/user1/data/observatory/cache" / name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def _cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from URL and parameters"""
        key_string = url
        if params:
            key_string += json.dumps(params, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path to cache file"""
        return self.cache_dir / f"{cache_key}.json"
    
    def _read_cache(self, cache_key: str, max_age_hours: int = 24) -> Optional[Dict]:
        """Read from cache if not expired"""
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        # Check age
        age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        if age > timedelta(hours=max_age_hours):
            return None
        
        try:
            with open(cache_path) as f:
                return json.load(f)
        except:
            return None
    
    def _write_cache(self, cache_key: str, data: Dict):
        """Write to cache"""
        cache_path = self._get_cache_path(cache_key)
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _log(self, message: str, level: str = "INFO"):
        """Simple logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.name}] {level}: {message}")
