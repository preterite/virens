#!/usr/bin/env python3
"""
Obsidian Vault → Observatory DB Sync
======================================
Walks the vault events directory, reads YAML frontmatter from each .md note,
and upserts into the appropriate DB table based on the frontmatter `type` field.

Routing (configured in observatory.yaml academic_events.sync_routing):
  speaking  → speaking table (dedicated CRUD)
  teaching  → teaching table (rare; bulk import preferred)
  publication, grant, service, editorial → academic_events table

Idempotent: running twice on unchanged vault state produces no changes.
"""

import sys
import yaml
import json
import logging
from pathlib import Path
from datetime import datetime

# Wire up observatory module imports
_obs_root = Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'
sys.path.insert(0, str(_obs_root))

from core.config import config
from core.database import db

logger = logging.getLogger('observatory.sync')


def load_sync_config() -> dict:
    """Load sync configuration from user observatory.yaml."""
    virens_file = Path.home() / '.virens'
    if virens_file.exists():
        user_dir = Path(virens_file.read_text().strip())
        config_file = user_dir / 'config' / 'observatory.yaml'
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
    return {}


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return {}

    # Find closing ---
    end = text.find('---', 3)
    if end == -1:
        return {}

    fm_text = text[3:end].strip()
    try:
        return yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        logger.error(f"YAML parse error in {filepath}: {e}")
        return {}


def _sanitize_value(val):
    """Convert non-JSON-serializable types (date, datetime) to strings."""
    from datetime import date as _date, datetime as _dt
    if isinstance(val, _dt):
        return val.isoformat()
    if isinstance(val, _date):
        return val.isoformat()
    if isinstance(val, list):
        return [_sanitize_value(v) for v in val]
    if isinstance(val, dict):
        return {k: _sanitize_value(v) for k, v in val.items()}
    return val


def _sanitize_frontmatter(fm: dict) -> dict:
    """Sanitize all values in frontmatter for JSON compatibility."""
    return {k: _sanitize_value(v) for k, v in fm.items()}


def _speaking_data_from_frontmatter(fm: dict, vault_path: str) -> dict:
    """Map frontmatter fields to speaking table columns."""
    return {
        'title': fm.get('title', ''),
        'venue': fm.get('venue', ''),
        'event_date': fm.get('event-date'),
        'invitation_date': fm.get('invitation-date'),
        'response_status': fm.get('response-status', 'invited'),
        'event_type': fm.get('event-type', ''),
        'honorarium': fm.get('honorarium'),
        'notes': fm.get('notes', ''),
        'vault_path': vault_path,
    }


def _academic_event_from_frontmatter(fm: dict, category: str, vault_path: str) -> dict:
    """Map frontmatter fields to academic_events table (core + metadata JSON)."""
    # Core fields
    event = {
        'category': category,
        'title': fm.get('title', ''),
        'status': fm.get('status', ''),
        'date_start': fm.get('date-start') or fm.get('date-submitted'),
        'date_end': fm.get('date-end'),
        'notes': fm.get('notes', ''),
        'vault_path': vault_path,
    }

    # Everything else goes into metadata
    core_keys = {
        'type', 'title', 'status', 'date-start', 'date-end', 'notes',
        'date-created', 'date-modified', 'tags'
    }
    metadata = {k: v for k, v in fm.items() if k not in core_keys and v is not None}
    event['metadata'] = metadata

    return event


def _teaching_data_from_frontmatter(fm: dict) -> dict:
    """Map frontmatter fields to teaching table columns."""
    return {
        'course_code': fm.get('course-code', ''),
        'course_name': fm.get('course-name') or fm.get('title', ''),
        'course_type': fm.get('course-type', ''),
        'semester': fm.get('semester', ''),
        'year': fm.get('year'),
        'start_date': fm.get('date-start'),
        'end_date': fm.get('date-end'),
        'notes': fm.get('notes', ''),
    }


def _normalize_val(v):
    """Normalize for comparison: None/'' → '', numeric types unified."""
    if v is None:
        return ''
    if isinstance(v, float) and v == int(v):
        return int(v)
    return v


def _records_equal_speaking(existing: dict, new_data: dict) -> bool:
    """Check if a speaking record matches new data (for idempotency)."""
    fields = ['title', 'venue', 'event_date', 'invitation_date',
              'response_status', 'event_type', 'honorarium', 'notes']
    for f in fields:
        old_val = _normalize_val(existing.get(f))
        new_val = _normalize_val(new_data.get(f))
        if old_val != new_val:
            return False
    return True


def _records_equal_academic(existing: dict, new_data: dict) -> bool:
    """Check if an academic_events record matches new data."""
    for key in ['category', 'title', 'status', 'date_start', 'date_end', 'notes']:
        old_val = existing.get(key)
        new_val = new_data.get(key)
        if (old_val or '') != (new_val or ''):
            if old_val is None and new_val is None:
                continue
            return False
    # Check metadata
    old_meta = existing.get('metadata', {})
    if isinstance(old_meta, str):
        try:
            old_meta = json.loads(old_meta)
        except (json.JSONDecodeError, TypeError):
            old_meta = {}
    new_meta = new_data.get('metadata', {})
    return old_meta == new_meta


def sync_vault(dry_run: bool = False) -> dict:
    """
    Walk the vault events directory, sync each note to the DB.
    Returns stats: {new: N, updated: N, unchanged: N, errors: N}
    """
    user_config = load_sync_config()
    ae_config = user_config.get('academic_events', {})

    if not ae_config.get('enabled', False):
        logger.info("Academic events sync is disabled in config")
        return {'new': 0, 'updated': 0, 'unchanged': 0, 'errors': 0}

    vault_dir_rel = ae_config.get('vault_directory', '000_observatory/events')
    sync_routing = ae_config.get('sync_routing', {})

    # Resolve vault root
    vault_root = Path.home() / 'Local/virens/user1/Scholar'
    events_dir = vault_root / vault_dir_rel

    if not events_dir.exists():
        logger.warning(f"Events directory does not exist: {events_dir}")
        return {'new': 0, 'updated': 0, 'unchanged': 0, 'errors': 0}

    stats = {'new': 0, 'updated': 0, 'unchanged': 0, 'errors': 0}

    # Walk all .md files in the events directory tree
    for md_file in sorted(events_dir.rglob('*.md')):
        fm = parse_frontmatter(md_file)
        if not fm:
            logger.debug(f"No frontmatter: {md_file.name}")
            continue

        # Sanitize date objects etc. for JSON compatibility
        fm = _sanitize_frontmatter(fm)

        event_type = fm.get('type')
        if not event_type:
            logger.debug(f"No type field: {md_file.name}")
            continue

        # Resolve relative vault path for tracking
        vault_path = str(md_file.relative_to(vault_root))
        target_table = sync_routing.get(event_type)

        if not target_table:
            logger.debug(f"No sync routing for type '{event_type}': {md_file.name}")
            continue

        try:
            if target_table == 'speaking':
                data = _speaking_data_from_frontmatter(fm, vault_path)
                existing = db.get_speaking_event_by_vault_path(vault_path)

                if existing:
                    if _records_equal_speaking(existing, data):
                        stats['unchanged'] += 1
                    else:
                        if not dry_run:
                            db.update_speaking_event(existing['id'], data)
                        stats['updated'] += 1
                        logger.info(f"Updated speaking: {data['title']}")
                else:
                    if not dry_run:
                        db.add_speaking_event_from_vault(data)
                    stats['new'] += 1
                    logger.info(f"Added speaking: {data['title']}")

            elif target_table == 'academic_events':
                data = _academic_event_from_frontmatter(fm, event_type, vault_path)

                # Check for existing by vault_path
                existing_events = db.get_academic_events()
                existing = None
                for ev in existing_events:
                    if ev.get('vault_path') == vault_path:
                        existing = ev
                        break

                if existing:
                    if _records_equal_academic(existing, data):
                        stats['unchanged'] += 1
                    else:
                        if not dry_run:
                            db.update_academic_event(existing['id'], {
                                'category': data['category'],
                                'title': data['title'],
                                'status': data['status'],
                                'date_start': data['date_start'],
                                'date_end': data['date_end'],
                                'notes': data['notes'],
                                'metadata': data['metadata'],
                            })
                        stats['updated'] += 1
                        logger.info(f"Updated {event_type}: {data['title']}")
                else:
                    if not dry_run:
                        db.add_academic_event(data)
                    stats['new'] += 1
                    logger.info(f"Added {event_type}: {data['title']}")

            elif target_table == 'teaching':
                data = _teaching_data_from_frontmatter(fm)
                # Teaching dedup: course_code + semester + year
                if not dry_run:
                    db.add_teaching_record(data)
                stats['new'] += 1
                logger.info(f"Added teaching: {data['course_name']}")

            else:
                logger.warning(f"Unknown target table '{target_table}' for {md_file.name}")
                stats['errors'] += 1

        except Exception as e:
            logger.error(f"Error syncing {md_file.name}: {e}")
            stats['errors'] += 1

    return stats


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    import argparse
    parser = argparse.ArgumentParser(description='Sync Obsidian vault events to Observatory DB')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be synced without writing to DB')
    args = parser.parse_args()

    print("Observatory Vault Sync")
    print(f"  Database: {config.database_path}")
    print(f"  Dry run:  {args.dry_run}")
    print()

    stats = sync_vault(dry_run=args.dry_run)

    print(f"\nSync complete:")
    print(f"  New:       {stats['new']}")
    print(f"  Updated:   {stats['updated']}")
    print(f"  Unchanged: {stats['unchanged']}")
    print(f"  Errors:    {stats['errors']}")


if __name__ == '__main__':
    main()
