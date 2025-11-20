#!/usr/bin/env python3
"""
Database management for Academic Observatory
SQLite-based storage for publications, citations, and metrics
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from contextlib import contextmanager
import json

from .config import config

class Database:
    """SQLite database manager for Observatory"""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = config.database_path
        self.db_path = db_path
        self.initialize()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def initialize(self):
        """Create database schema if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Publications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS publications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    year INTEGER,
                    authors TEXT,
                    venue TEXT,
                    publication_type TEXT,
                    doi TEXT,
                    url TEXT,
                    semantic_scholar_id TEXT UNIQUE,
                    openalex_id TEXT,
                    abstract TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Citations table (time-series data)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS citations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    publication_id INTEGER NOT NULL,
                    citation_count INTEGER NOT NULL,
                    source TEXT NOT NULL,
                    fetched_at TEXT NOT NULL,
                    FOREIGN KEY (publication_id) REFERENCES publications(id)
                )
            ''')
            
            # Metrics table (aggregate metrics over time)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metadata TEXT,
                    recorded_at TEXT NOT NULL
                )
            ''')
            
            # Peers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS peers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    orcid TEXT,
                    semantic_scholar_id TEXT,
                    openalex_id TEXT,
                    h_index INTEGER,
                    citation_count INTEGER,
                    paper_count INTEGER,
                    notes TEXT,
                    added_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Field monitoring (relevant papers in your fields)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS field_papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    authors TEXT,
                    venue TEXT,
                    year INTEGER,
                    abstract TEXT,
                    keywords TEXT,
                    relevance_score REAL,
                    semantic_scholar_id TEXT UNIQUE,
                    openalex_id TEXT,
                    discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Teaching metrics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teaching (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_code TEXT,
                    course_name TEXT,
                    course_type TEXT,
                    semester TEXT,
                    year INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    notes TEXT
                )
            ''')
            
            # Speaking invitations & events
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS speaking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    venue TEXT,
                    event_date TEXT,
                    invitation_date TEXT,
                    response_status TEXT,
                    event_type TEXT,
                    honorarium REAL,
                    notes TEXT
                )
            ''')
            
            # External metrics (GitHub, website analytics, etc.)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS external_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value TEXT,
                    metadata TEXT,
                    fetched_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes for common queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_citations_pub_id 
                ON citations(publication_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_citations_date 
                ON citations(fetched_at)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_metrics_type_date 
                ON metrics(metric_type, recorded_at)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_field_papers_relevance
                ON field_papers(relevance_score)
            ''')
            
            print(f"✓ Database initialized at {self.db_path}")
    
    def add_publication(self, pub_data: Dict[str, Any]) -> int:
        """Add or update a publication"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if publication exists (by semantic_scholar_id or title+year)
            semantic_id = pub_data.get('semantic_scholar_id')
            
            if semantic_id:
                cursor.execute(
                    'SELECT id FROM publications WHERE semantic_scholar_id = ?',
                    (semantic_id,)
                )
            else:
                # Fallback: match by title and year
                cursor.execute(
                    'SELECT id FROM publications WHERE title = ? AND year = ?',
                    (pub_data.get('title'), pub_data.get('year'))
                )
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing
                pub_id = existing['id']
                cursor.execute('''
                    UPDATE publications SET
                        title = ?, year = ?, authors = ?, venue = ?,
                        publication_type = ?, doi = ?, url = ?, 
                        semantic_scholar_id = ?, openalex_id = ?,
                        abstract = ?, updated_at = ?
                    WHERE id = ?
                ''', (
                    pub_data.get('title'),
                    pub_data.get('year'),
                    pub_data.get('authors'),
                    pub_data.get('venue'),
                    pub_data.get('publication_type'),
                    pub_data.get('doi'),
                    pub_data.get('url'),
                    pub_data.get('semantic_scholar_id'),
                    pub_data.get('openalex_id'),
                    pub_data.get('abstract'),
                    datetime.now().isoformat(),
                    pub_id
                ))
            else:
                # Insert new
                cursor.execute('''
                    INSERT INTO publications 
                    (title, year, authors, venue, publication_type, doi, url,
                     semantic_scholar_id, openalex_id, abstract)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pub_data.get('title'),
                    pub_data.get('year'),
                    pub_data.get('authors'),
                    pub_data.get('venue'),
                    pub_data.get('publication_type'),
                    pub_data.get('doi'),
                    pub_data.get('url'),
                    pub_data.get('semantic_scholar_id'),
                    pub_data.get('openalex_id'),
                    pub_data.get('abstract')
                ))
                pub_id = cursor.lastrowid
            
            return pub_id
    
    def add_citation_count(self, publication_id: int, count: int, source: str):
        """Record a citation count for a publication"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO citations (publication_id, citation_count, source, fetched_at)
                VALUES (?, ?, ?, ?)
            ''', (publication_id, count, source, datetime.now().isoformat()))
    
    def add_metric(self, metric_type: str, value: float, metadata: Optional[Dict] = None):
        """Record a metric value"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metrics (metric_type, metric_value, metadata, recorded_at)
                VALUES (?, ?, ?, ?)
            ''', (
                metric_type,
                value,
                json.dumps(metadata) if metadata else None,
                datetime.now().isoformat()
            ))
    
    def get_publications(self) -> List[Dict[str, Any]]:
        """Get all publications"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM publications ORDER BY year DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_publication_by_id(self, pub_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific publication by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM publications WHERE id = ?', (pub_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_latest_citations(self) -> List[Tuple[str, int, int]]:
        """Get latest citation counts for all publications (title, year, count)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.title, p.year, COALESCE(c.citation_count, 0) as citations
                FROM publications p
                LEFT JOIN citations c ON p.id = c.publication_id
                WHERE c.id IN (
                    SELECT MAX(id) FROM citations GROUP BY publication_id
                ) OR c.id IS NULL
                ORDER BY p.year DESC
            ''')
            return cursor.fetchall()
    
    def get_citation_history(self, publication_id: int) -> List[Dict]:
        """Get citation history for a specific publication"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT citation_count, source, fetched_at
                FROM citations
                WHERE publication_id = ?
                ORDER BY fetched_at
            ''', (publication_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_metrics_history(self, metric_type: str, days: int = 90) -> List[Dict]:
        """Get metric history for charting"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT metric_value, recorded_at, metadata
                FROM metrics
                WHERE metric_type = ?
                AND recorded_at >= date('now', '-' || ? || ' days')
                ORDER BY recorded_at
            ''', (metric_type, days))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_latest_metric(self, metric_type: str) -> Optional[float]:
        """Get the most recent value for a metric"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT metric_value
                FROM metrics
                WHERE metric_type = ?
                ORDER BY recorded_at DESC
                LIMIT 1
            ''', (metric_type,))
            row = cursor.fetchone()
            return row['metric_value'] if row else None
    
    def add_teaching_record(self, course_data: Dict[str, Any]):
        """Add a teaching record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO teaching 
                (course_code, course_name, course_type, semester, year, 
                 start_date, end_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_data.get('course_code'),
                course_data.get('course_name'),
                course_data.get('course_type'),
                course_data.get('semester'),
                course_data.get('year'),
                course_data.get('start_date'),
                course_data.get('end_date'),
                course_data.get('notes')
            ))
    
    def get_teaching_summary(self, year: Optional[int] = None) -> Dict[str, Any]:
        """Get teaching load summary"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if year:
                cursor.execute('''
                    SELECT course_type, COUNT(*) as count
                    FROM teaching
                    WHERE year = ?
                    GROUP BY course_type
                ''', (year,))
            else:
                cursor.execute('''
                    SELECT year, course_type, COUNT(*) as count
                    FROM teaching
                    GROUP BY year, course_type
                    ORDER BY year DESC
                ''')
            
            return [dict(row) for row in cursor.fetchall()]
    
    def add_speaking_event(self, event_data: Dict[str, Any]):
        """Add a speaking invitation/event"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO speaking
                (title, venue, event_date, invitation_date, response_status,
                 event_type, honorarium, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data.get('title'),
                event_data.get('venue'),
                event_data.get('event_date'),
                event_data.get('invitation_date'),
                event_data.get('response_status'),
                event_data.get('event_type'),
                event_data.get('honorarium'),
                event_data.get('notes')
            ))
    
    def get_speaking_events(self, year: Optional[int] = None) -> List[Dict]:
        """Get speaking events"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if year:
                cursor.execute('''
                    SELECT * FROM speaking
                    WHERE strftime('%Y', event_date) = ?
                    ORDER BY event_date DESC
                ''', (str(year),))
            else:
                cursor.execute('''
                    SELECT * FROM speaking
                    ORDER BY event_date DESC
                ''')
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overall database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Publications count
            cursor.execute('SELECT COUNT(*) as count FROM publications')
            stats['publications'] = cursor.fetchone()['count']
            
            # Citation data points
            cursor.execute('SELECT COUNT(*) as count FROM citations')
            stats['citation_records'] = cursor.fetchone()['count']
            
            # Metrics data points
            cursor.execute('SELECT COUNT(*) as count FROM metrics')
            stats['metric_records'] = cursor.fetchone()['count']
            
            # Teaching records
            cursor.execute('SELECT COUNT(*) as count FROM teaching')
            stats['teaching_records'] = cursor.fetchone()['count']
            
            # Speaking events
            cursor.execute('SELECT COUNT(*) as count FROM speaking')
            stats['speaking_events'] = cursor.fetchone()['count']

                        
            return stats
                
    def add_external_metric(self, source: str, metric_name: str, 
                                      metric_value: str, metadata: Optional[Dict], 
                                      fetched_at: str):
                    """Add an external metric (GitHub, website analytics, etc.)"""
                    with self.get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO external_metrics 
                            (source, metric_name, metric_value, metadata, fetched_at)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            source,
                            metric_name,
                            metric_value,
                            json.dumps(metadata) if metadata else None,
                            fetched_at
                        ))
            
# Global database instance
db = Database()
