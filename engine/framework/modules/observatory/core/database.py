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
            
            # Academic events (publications, grants, service, editorial)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS academic_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    status TEXT,
                    date_created TEXT DEFAULT CURRENT_TIMESTAMP,
                    date_modified TEXT DEFAULT CURRENT_TIMESTAMP,
                    date_start TEXT,
                    date_end TEXT,
                    notes TEXT,
                    vault_path TEXT,
                    metadata TEXT
                )
            ''')

            # Add vault_path to speaking table if missing (migration)
            cursor.execute("PRAGMA table_info(speaking)")
            speaking_cols = [row[1] for row in cursor.fetchall()]
            if 'vault_path' not in speaking_cols:
                cursor.execute('ALTER TABLE speaking ADD COLUMN vault_path TEXT')

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
            
            # Check if publication exists (by semantic_scholar_id, DOI, or title+year)
            semantic_id = pub_data.get('semantic_scholar_id')
            doi = pub_data.get('doi')
            existing = None

            if semantic_id:
                cursor.execute(
                    'SELECT id FROM publications WHERE semantic_scholar_id = ?',
                    (semantic_id,)
                )
                existing = cursor.fetchone()

            if not existing and doi:
                cursor.execute(
                    'SELECT id FROM publications WHERE doi = ?',
                    (doi,)
                )
                existing = cursor.fetchone()

            if not existing:
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
    def add_field_paper(self, paper: Dict[str, Any]):
        """Add or update a field paper record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            openalex_id = paper.get('openalex_id')
            if openalex_id:
                cursor.execute('SELECT id FROM field_papers WHERE openalex_id = ?', (openalex_id,))
                existing = cursor.fetchone()
                if existing:
                    cursor.execute('''
                        UPDATE field_papers SET
                            title = ?, authors = ?, venue = ?, year = ?,
                            abstract = ?, keywords = ?, relevance_score = ?,
                            openalex_id = ?
                        WHERE id = ?
                    ''', (
                        paper.get('title'),
                        ', '.join(paper.get('authors', [])) if isinstance(paper.get('authors'), list) else paper.get('authors'),
                        paper.get('journal'),
                        paper.get('year'),
                        paper.get('abstract'),
                        ', '.join(paper.get('matched_keywords', [])) if isinstance(paper.get('matched_keywords'), list) else paper.get('matched_keywords'),
                        paper.get('relevance_score'),
                        openalex_id,
                        existing['id']
                    ))
                    return
            cursor.execute('''
                INSERT INTO field_papers
                (title, authors, venue, year, abstract, keywords, relevance_score, openalex_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                paper.get('title'),
                ', '.join(paper.get('authors', [])) if isinstance(paper.get('authors'), list) else paper.get('authors'),
                paper.get('journal'),
                paper.get('year'),
                paper.get('abstract'),
                ', '.join(paper.get('matched_keywords', [])) if isinstance(paper.get('matched_keywords'), list) else paper.get('matched_keywords'),
                paper.get('relevance_score'),
                paper.get('openalex_id')
            ))

    def add_academic_event(self, event_data: Dict[str, Any]) -> int:
        """Add or update an academic event. metadata should be a dict (gets JSON-serialized)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            vault_path = event_data.get('vault_path')
            if vault_path:
                cursor.execute(
                    'SELECT id FROM academic_events WHERE vault_path = ?',
                    (vault_path,)
                )
                existing = cursor.fetchone()
            else:
                existing = None

            metadata = event_data.get('metadata')
            if isinstance(metadata, dict):
                metadata = json.dumps(metadata)

            if existing:
                event_id = existing['id']
                cursor.execute('''
                    UPDATE academic_events SET
                        category = ?, title = ?, status = ?,
                        date_modified = ?, date_start = ?, date_end = ?,
                        notes = ?, vault_path = ?, metadata = ?
                    WHERE id = ?
                ''', (
                    event_data.get('category'),
                    event_data.get('title'),
                    event_data.get('status'),
                    datetime.now().isoformat(),
                    event_data.get('date_start'),
                    event_data.get('date_end'),
                    event_data.get('notes'),
                    vault_path,
                    metadata,
                    event_id
                ))
                return event_id
            else:
                cursor.execute('''
                    INSERT INTO academic_events
                    (category, title, status, date_created, date_modified,
                     date_start, date_end, notes, vault_path, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event_data.get('category'),
                    event_data.get('title'),
                    event_data.get('status'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    event_data.get('date_start'),
                    event_data.get('date_end'),
                    event_data.get('notes'),
                    vault_path,
                    metadata
                ))
                return cursor.lastrowid

    def get_academic_events(self, category: Optional[str] = None,
                            status: Optional[str] = None,
                            year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get academic events with optional filters."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM academic_events WHERE 1=1'
            params = []
            if category:
                query += ' AND category = ?'
                params.append(category)
            if status:
                query += ' AND status = ?'
                params.append(status)
            if year:
                query += ' AND (strftime("%Y", date_start) = ? OR strftime("%Y", date_created) = ?)'
                params.extend([str(year), str(year)])
            query += ' ORDER BY date_modified DESC'
            cursor.execute(query, params)
            rows = [dict(row) for row in cursor.fetchall()]
            # Deserialize metadata JSON
            for row in rows:
                if row.get('metadata'):
                    try:
                        row['metadata'] = json.loads(row['metadata'])
                    except (json.JSONDecodeError, TypeError):
                        pass
            return rows

    def update_academic_event(self, event_id: int, updates: Dict[str, Any]) -> bool:
        """Update specific fields of an academic event."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            allowed = {'category', 'title', 'status', 'date_start', 'date_end',
                        'notes', 'vault_path', 'metadata'}
            set_clauses = ['date_modified = ?']
            params = [datetime.now().isoformat()]

            for key, val in updates.items():
                if key not in allowed:
                    continue
                if key == 'metadata' and isinstance(val, dict):
                    val = json.dumps(val)
                set_clauses.append(f'{key} = ?')
                params.append(val)

            if len(set_clauses) == 1:
                return False  # nothing to update

            params.append(event_id)
            cursor.execute(
                f'UPDATE academic_events SET {", ".join(set_clauses)} WHERE id = ?',
                params
            )
            return cursor.rowcount > 0

    def get_speaking_event_by_vault_path(self, vault_path: str) -> Optional[Dict[str, Any]]:
        """Get a speaking event by its vault_path."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM speaking WHERE vault_path = ?',
                           (vault_path,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def add_speaking_event_from_vault(self, event_data: Dict[str, Any]) -> int:
        """Add a speaking event with vault_path tracking."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO speaking
                (title, venue, event_date, invitation_date, response_status,
                 event_type, honorarium, notes, vault_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data.get('title'),
                event_data.get('venue'),
                event_data.get('event_date'),
                event_data.get('invitation_date'),
                event_data.get('response_status'),
                event_data.get('event_type'),
                event_data.get('honorarium'),
                event_data.get('notes'),
                event_data.get('vault_path')
            ))
            return cursor.lastrowid

    def update_speaking_event(self, event_id: int, event_data: Dict[str, Any]):
        """Update a speaking event by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE speaking SET
                    title = ?, venue = ?, event_date = ?, invitation_date = ?,
                    response_status = ?, event_type = ?, honorarium = ?,
                    notes = ?, vault_path = ?
                WHERE id = ?
            ''', (
                event_data.get('title'),
                event_data.get('venue'),
                event_data.get('event_date'),
                event_data.get('invitation_date'),
                event_data.get('response_status'),
                event_data.get('event_type'),
                event_data.get('honorarium'),
                event_data.get('notes'),
                event_data.get('vault_path'),
                event_id
            ))


# Global database instance
db = Database()
