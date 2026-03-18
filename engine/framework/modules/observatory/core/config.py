#!/usr/bin/env python3
"""
Observatory Core Config — VIRENS-native
Replaces the old SRE-hardcoded Config class.
Loads user1/config/observatory.yaml via the load_config() merger.
"""

import sys
from pathlib import Path

# Add user1/observatory to path so we can import load_config
_user_obs = Path.home() / 'Local' / 'virens' / 'user1' / 'observatory'
if str(_user_obs) not in sys.path:
    sys.path.insert(0, str(_user_obs))

from config import load_config as _load_config

class ConfigAdapter:
    """
    Translates the YAML config structure into the attribute-style interface
    that the analyzers and fetchers expect (config.email, config.database_path, etc.)
    """
    def __init__(self):
        self._config = _load_config()
        user_root = Path.home() / 'Local' / 'virens' / 'user1'
        self.sre_home   = user_root          # legacy name
        self.data_dir   = user_root / 'data'
        self.observatory_data = self.data_dir / 'observatory'
        self.cache_dir  = self.observatory_data / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def database_path(self) -> Path:
        return Path(self._config['database']['path'])

    @property
    def email(self) -> str:
        return self._config['api_credentials']['openalex']['email']

    def get_api_key(self, service: str) -> str:
        if service == 'semantic_scholar':
            return self._config['api_credentials']['semantic_scholar']['api_key']
        elif service == 'github':
            return self._config['api_credentials']['github']['token']
        elif service == 'crossref':
            return self._config['api_credentials']['crossref'].get('api_key', '')
        elif service == 'plausible':
            return self._config['api_credentials']['plausible'].get('api_key', '')
        raise ValueError(f"Unknown service: {service}")

    def get_orcid_id(self) -> str:
        return self._config['researcher']['orcid_id']

    def get_github_username(self) -> str:
        return self._config['api_credentials']['github']['username']

    def __getitem__(self, key):
        return self._config[key]

    def get(self, key, default=None):
        return self._config.get(key, default)


config = ConfigAdapter()
