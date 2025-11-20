#!/usr/bin/env python3
"""
Configuration management for Academic Observatory
Adjusted for existing SRE structure
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Centralized configuration management"""
    
    def __init__(self, sre_home: Optional[Path] = None):
        if sre_home is None:
            sre_home = Path.home() / "AcademicSync" / "SRE"
        
        self.sre_home = Path(sre_home)
        self.data_dir = self.sre_home / "data"
        self.config_dir = self.data_dir / "config"
        self.observatory_data = self.data_dir / "observatory"
        self.cache_dir = self.observatory_data / "cache"
        
        # Ensure directories exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configurations (lazy loading)
        self._credentials = None
        self._peers = None
        self._journals = None
        self._thresholds = None
        self._fields = None
    
    @property
    def credentials(self) -> Dict[str, Any]:
        """Load credentials (lazy loading)"""
        if self._credentials is None:
            cred_file = self.config_dir / "credentials.json"
            if cred_file.exists():
                with open(cred_file) as f:
                    self._credentials = json.load(f)
            else:
                raise FileNotFoundError(
                    f"Credentials file not found: {cred_file}\n"
                    f"Copy credentials.json.template and add your API keys"
                )
        return self._credentials
    
    @property
    def peers(self) -> Dict[str, Any]:
        """Load peer researchers configuration"""
        if self._peers is None:
            with open(self.config_dir / "peers.json") as f:
                self._peers = json.load(f)
        return self._peers
    
    @property
    def journals(self) -> Dict[str, Any]:
        """Load monitored journals configuration"""
        if self._journals is None:
            with open(self.config_dir / "journals.json") as f:
                self._journals = json.load(f)
        return self._journals
    
    @property
    def thresholds(self) -> Dict[str, Any]:
        """Load notification thresholds configuration"""
        if self._thresholds is None:
            with open(self.config_dir / "thresholds.json") as f:
                self._thresholds = json.load(f)
        return self._thresholds
    
    @property
    def fields(self) -> Dict[str, Any]:
        """Load monitored fields and keywords"""
        if self._fields is None:
            with open(self.config_dir / "fields.json") as f:
                self._fields = json.load(f)
        return self._fields
    
    @property
    def database_path(self) -> Path:
        """Get path to SQLite database"""
        return self.observatory_data / "observatory.db"
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        return self.credentials.get(service, {}).get("api_key")
    
    def is_service_enabled(self, service: str) -> bool:
        """Check if a service is enabled"""
        service_config = self.credentials.get(service, {})
        return service_config.get("enabled", True)  # Default to enabled
    
    def save_peers(self):
        """Save updated peers configuration"""
        with open(self.config_dir / "peers.json", 'w') as f:
            json.dump(self._peers, f, indent=2)
    
    def __repr__(self):
        return f"Config(sre_home={self.sre_home}, db={self.database_path})"

# Global config instance
config = Config()
