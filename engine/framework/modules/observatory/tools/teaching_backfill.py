#!/usr/bin/env python3
"""
Teaching Backfill Utility
==========================
Insert historical course data (2020–2024) into the observatory `teaching` table.

Usage:
  1. Edit the COURSES list below with actual course data, OR
  2. Pass a YAML file: python3 teaching_backfill.py --file courses.yaml

YAML format:
  - course_code: "ENGL 101"
    course_name: "College Composition"
    course_type: "first_year_composition"
    semester: "Fall"
    year: 2020
    start_date: "2020-08-24"
    end_date: "2020-12-18"
    notes: ""

Skips duplicates (by course_code + semester + year).
"""

import sys
import yaml
import logging
from pathlib import Path

# Wire up observatory imports
_obs_root = Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'
sys.path.insert(0, str(_obs_root))

from core.config import config
from core.database import db

logger = logging.getLogger('observatory.teaching_backfill')


def classify_course_type(course_code: str, user_config: dict) -> str:
    """Classify a course using config rules, falling back to manual spec."""
    import re

    course_types = (user_config
                    .get('teaching_import', {})
                    .get('course_types', {}))

    for type_key, type_def in course_types.items():
        patterns = type_def.get('match_patterns', [])
        for pattern in patterns:
            if isinstance(pattern, str):
                # Simple string match
                if pattern.lower() in course_code.lower():
                    return type_def.get('label', type_key)
            elif isinstance(pattern, dict):
                # Prefix + number range
                prefix = pattern.get('prefix', '')
                num_range = pattern.get('number_range', [0, 999])
                if course_code.upper().startswith(prefix.upper()):
                    # Extract number
                    match = re.search(r'(\d+)', course_code[len(prefix):])
                    if match:
                        num = int(match.group(1))
                        if num_range[0] <= num <= num_range[1]:
                            return type_def.get('label', type_key)

    return 'Undergraduate'  # default fallback


def load_user_config() -> dict:
    """Load user observatory config."""
    virens_file = Path.home() / '.virens'
    if virens_file.exists():
        user_dir = Path(virens_file.read_text().strip())
        config_file = user_dir / 'config' / 'observatory.yaml'
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
    return {}


def check_duplicate(course_code: str, semester: str, year: int) -> bool:
    """Check if a course record already exists."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM teaching
            WHERE course_code = ? AND semester = ? AND year = ?
        ''', (course_code, semester, year))
        return cursor.fetchone() is not None


def backfill(courses: list, dry_run: bool = False) -> dict:
    """Insert courses, skipping duplicates. Returns stats."""
    user_config = load_user_config()
    stats = {'inserted': 0, 'skipped': 0, 'errors': 0}

    for course in courses:
        code = course.get('course_code', '')
        semester = course.get('semester', '')
        year = course.get('year')

        if not code or not year:
            logger.warning(f"Skipping incomplete record: {course}")
            stats['errors'] += 1
            continue

        if check_duplicate(code, semester, year):
            logger.info(f"Skipping duplicate: {code} {semester} {year}")
            stats['skipped'] += 1
            continue

        # Auto-classify if course_type not provided
        if not course.get('course_type'):
            course['course_type'] = classify_course_type(code, user_config)

        if dry_run:
            logger.info(f"Would insert: {code} {semester} {year} ({course['course_type']})")
        else:
            try:
                db.add_teaching_record(course)
                logger.info(f"Inserted: {code} {semester} {year} ({course['course_type']})")
            except Exception as e:
                logger.error(f"Error inserting {code}: {e}")
                stats['errors'] += 1
                continue

        stats['inserted'] += 1

    return stats


def main():
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    parser = argparse.ArgumentParser(description='Backfill teaching data into Observatory DB')
    parser.add_argument('--file', '-f', type=str,
                        help='Path to YAML file with course data')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be inserted without writing to DB')
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"File not found: {filepath}")
            sys.exit(1)
        with open(filepath) as f:
            courses = yaml.safe_load(f)
    else:
        print("No --file provided. Edit the COURSES list in this script or provide a YAML file.")
        print("Usage: python3 teaching_backfill.py --file courses.yaml [--dry-run]")
        sys.exit(0)

    print("Teaching Backfill")
    print(f"  Database: {config.database_path}")
    print(f"  Courses:  {len(courses)}")
    print(f"  Dry run:  {args.dry_run}")
    print()

    stats = backfill(courses, dry_run=args.dry_run)

    print(f"\nBackfill complete:")
    print(f"  Inserted: {stats['inserted']}")
    print(f"  Skipped:  {stats['skipped']}")
    print(f"  Errors:   {stats['errors']}")


if __name__ == '__main__':
    main()
