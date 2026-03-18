#!/usr/bin/env python3
"""
GitHub API fetcher
Repository statistics and activity metrics
Requires personal access token
"""
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
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

# GitHub-specific configuration
GITHUB_CONFIG = _user_config.get('github', {})
GITHUB_USERNAME = GITHUB_CONFIG.get('username', 'github-user')
ACADEMIC_KEYWORDS = GITHUB_CONFIG.get('academic_keywords', [
    'research', 'academic', 'scholar', 'science', 'study'
])
TRACKED_REPOS = GITHUB_CONFIG.get('tracked_repos', [])

# Import observatory modules (no sys.path hack needed in new structure)
from observatory.core.config import config
from observatory.core.database import db
from observatory.fetchers.base import BaseFetcher

class GitHubFetcher(BaseFetcher):
    """Fetch data from GitHub API"""

    def __init__(self, include_private: bool = True):
        super().__init__("github", rate_limit_delay=1.0)
        # Username from user config (loaded at module level)
        self.username = GITHUB_USERNAME
        # Token from config system
        try:
            self.token = config.get_api_key('github')
        except (ValueError, KeyError):
            self.token = None
        self.base_url = "https://api.github.com"
        self.include_private = include_private
        
        if not self.token:
            self._log("WARNING: No GitHub token found, using unauthenticated API (very low rate limits)", "WARN")
            self.include_private = False
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with authentication and caching"""
        url = f"{self.base_url}/{endpoint}"
        
        # Check cache first (shorter cache for GitHub - 6 hours)
        cache_key = self._cache_key(url, params)
        cached = self._read_cache(cache_key, max_age_hours=6)
        if cached:
            self._log(f"Using cached data for {endpoint}")
            return cached
        
        # Rate limit
        self._rate_limit()
        
        # Setup headers
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
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
    
    def get_user_info(self) -> Optional[Dict]:
        """Get basic user information"""
        return self._make_request(f"users/{self.username}", {})
    
    def get_repositories(self, include_private: Optional[bool] = None) -> List[Dict]:
        """Get all repositories (public and optionally private)"""
        if include_private is None:
            include_private = self.include_private
        
        # Use /user/repos for authenticated requests (includes private)
        # Use /users/{username}/repos for unauthenticated (public only)
        if self.token and include_private:
            endpoint = "user/repos"
        else:
            endpoint = f"users/{self.username}/repos"
        
        params = {
            "type": "all" if include_private else "owner",
            "sort": "updated",
            "per_page": 100
        }
        
        data = self._make_request(endpoint, params)
        
        if data and isinstance(data, list):
            if include_private:
                self._log(f"Found {len(data)} repositories (including private)")
            else:
                self._log(f"Found {len(data)} public repositories")
            return data
        
        return []
    
    def get_commit_activity(self, days: int = 90, include_private: Optional[bool] = None) -> Dict[str, Any]:
        """Get commit activity across all repos for the last N days"""
        if include_private is None:
            include_private = self.include_private
        
        repos = self.get_repositories(include_private=include_private)
        
        # Get commits from each repo
        total_commits = 0
        commits_by_date = {}
        commits_by_repo = {}
        private_repos_with_commits = 0
        
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        for repo in repos:
            repo_name = repo["name"]
            is_private = repo.get("private", False)
            
            params = {
                "author": self.username,
                "since": since,
                "per_page": 100
            }
            
            # Use authenticated endpoint for private repos
            if self.token and is_private:
                commits = self._make_request(
                    f"repos/{self.username}/{repo_name}/commits",
                    params
                )
            else:
                commits = self._make_request(
                    f"repos/{self.username}/{repo_name}/commits",
                    params
                )
            
            if commits and isinstance(commits, list):
                repo_commit_count = len(commits)
                total_commits += repo_commit_count
                
                if repo_commit_count > 0:
                    commits_by_repo[repo_name] = {
                        "count": repo_commit_count,
                        "private": is_private
                    }
                    
                    if is_private:
                        private_repos_with_commits += 1
                
                # Group by date
                for commit in commits:
                    commit_date = commit["commit"]["author"]["date"][:10]  # YYYY-MM-DD
                    commits_by_date[commit_date] = commits_by_date.get(commit_date, 0) + 1
        
        self._log(f"Found {total_commits} commits in last {days} days")
        if include_private:
            self._log(f"  Including {private_repos_with_commits} private repos with activity")
        
        return {
            "total_commits": total_commits,
            "by_date": commits_by_date,
            "by_repo": commits_by_repo,
            "private_repos_active": private_repos_with_commits
        }
    
    def get_repository_stats(self, include_private: Optional[bool] = None) -> List[Dict]:
        """Get stats for key repositories"""
        if include_private is None:
            include_private = self.include_private
        
        repos = self.get_repositories(include_private=include_private)
        
        stats = []
        
        # Focus on repos that might be academic/research related
        # Keywords from user config (loaded at module level as ACADEMIC_KEYWORDS)
        academic_keywords = ACADEMIC_KEYWORDS
                
        for repo in repos:
            repo_name = repo["name"].lower()
            
            # Check if likely academic
            is_academic = any(keyword in repo_name for keyword in academic_keywords)
            
            stat = {
                "name": repo["name"],
                "description": repo.get("description", ""),
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "watchers": repo["watchers_count"],
                "updated_at": repo["updated_at"],
                "is_academic": is_academic,
                "is_private": repo.get("private", False),
                "url": repo["html_url"]
            }
            
            stats.append(stat)
        
        # Sort by updated date (most recent first)
        stats.sort(key=lambda x: x["updated_at"], reverse=True)
        
        return stats
    
    def update_metrics(self, include_private: Optional[bool] = None):
        """Update GitHub metrics in database"""
        if include_private is None:
            include_private = self.include_private
        
        timestamp = datetime.now().isoformat()
        
        # Get user info
        user_info = self.get_user_info()
        if user_info:
            db.add_external_metric(
                source="github",
                metric_name="public_repos",
                metric_value=str(user_info.get("public_repos", 0)),
                metadata=None,
                fetched_at=timestamp
            )
            
            db.add_external_metric(
                source="github",
                metric_name="followers",
                metric_value=str(user_info.get("followers", 0)),
                metadata=None,
                fetched_at=timestamp
            )
        
        # Get commit activity (last 90 days)
        activity = self.get_commit_activity(days=90, include_private=include_private)
        total_commits = activity["total_commits"]
        
        db.add_external_metric(
            source="github",
            metric_name="commits_90d",
            metric_value=str(total_commits),
            metadata={
                "by_date": activity["by_date"],
                "includes_private": include_private,
                "private_repos_active": activity["private_repos_active"]
            },
            fetched_at=timestamp
        )
        
        self._log(f"Recorded {total_commits} commits in last 90 days")
        if include_private:
            self._log(f"  Including {activity['private_repos_active']} active private repos")
        
        # Get repository stats
        repo_stats = self.get_repository_stats(include_private=include_private)
        
        # Count private repos
        private_count = sum(1 for r in repo_stats if r["is_private"])
        
        db.add_external_metric(
            source="github",
            metric_name="total_repos",
            metric_value=str(len(repo_stats)),
            metadata={"private_count": private_count},
            fetched_at=timestamp
        )
        
        # Track user-configured repos (from config: github.tracked_repos)
        if TRACKED_REPOS:
            # User has specified repos to track
            for tracked_name in TRACKED_REPOS:
                tracked_repo = next(
                    (r for r in repo_stats if tracked_name.lower() in r["name"].lower()), 
                    None
                )
                
                if tracked_repo:
                    # Sanitize repo name for metric name (replace hyphens/spaces with underscores)
                    safe_name = tracked_name.replace('-', '_').replace(' ', '_').lower()
                    metric_name = f"{safe_name}_repo_stars"
                    
                    db.add_external_metric(
                        source="github",
                        metric_name=metric_name,
                        metric_value=str(tracked_repo["stars"]),
                        metadata={
                            "name": tracked_repo["name"],
                            "url": tracked_repo["url"],
                            "private": tracked_repo["is_private"],
                            "tracked_repo_config": tracked_name  # Record what user asked for
                        },
                        fetched_at=timestamp
                    )
        else:
            # No tracked repos configured - track top 3 repos by stars
            top_repos = sorted(repo_stats, key=lambda r: r["stars"], reverse=True)[:3]
            for i, repo in enumerate(top_repos, 1):
                db.add_external_metric(
                    source="github",
                    metric_name=f"top_repo_{i}_stars",
                    metric_value=str(repo["stars"]),
                    metadata={
                        "name": repo["name"],
                        "url": repo["url"],
                        "private": repo["is_private"],
                        "rank": i
                    },
                    fetched_at=timestamp
                )
                        
        # Record total stars across all public repos only (stars on private repos aren't meaningful)
        public_repos = [r for r in repo_stats if not r["is_private"]]
        total_stars = sum(r["stars"] for r in public_repos)
        db.add_external_metric(
            source="github",
            metric_name="total_stars",
            metric_value=str(total_stars),
            metadata={"public_repos_only": True},
            fetched_at=timestamp
        )
        
        self._log(f"Updated GitHub metrics: {total_commits} commits, {total_stars} total stars")
        self._log(f"  Tracked {len(repo_stats)} repos ({private_count} private)")
    
    def get_contribution_summary(self) -> Dict[str, Any]:
        """Get a summary of GitHub contributions for display"""
        # Get recent metrics from database
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT metric_name, metric_value, metadata
                FROM external_metrics
                WHERE source = 'github'
                AND id IN (
                    SELECT MAX(id)
                    FROM external_metrics
                    WHERE source = 'github'
                    GROUP BY metric_name
                )
            ''')
            
            metrics = {}
            for row in cursor.fetchall():
                metrics[row['metric_name']] = {
                    'value': row['metric_value'],
                    'metadata': row['metadata']
                }
        
        return metrics

def fetch_github_data(include_private: bool = True):
    """Convenience function to fetch all GitHub data"""
    fetcher = GitHubFetcher(include_private=include_private)
    fetcher.update_metrics()

if __name__ == "__main__":
    fetch_github_data(include_private=True)
