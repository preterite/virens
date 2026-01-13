# VIRENS Timing.app Integration

Track time automatically, correlate with git commits, analyze writing and reading productivity, and surface insights through the Observatory dashboard.

## Overview

This module integrates [Timing.app](https://timingapp.com/) (macOS automatic time tracker) into the VIRENS research workflow, providing:

- **Automatic time tracking** via Timing's rule-based categorization
- **SQLite cache** for querying and analysis outside Timing
- **Git correlation** to connect coding hours with commit activity
- **Writing analysis** to identify peak creative hours
- **Reading analysis** to track research throughput
- **Observatory integration** for unified dashboard viewing
- **Weekly digests** with macOS notifications

## Prerequisites

- **Timing.app 2026.1+** (macOS, paid license required)
- **VIRENS user instance** at `~/Local/virens/user1/`
- **Observatory module** configured with database at `~/Local/virens/user1/data/observatory.db`
- **Python 3.9+** with standard library (no additional packages required)

## Quick Install
```bash
# From VIRENS framework directory
cd ~/Local/virens/virens/engine/framework/modules/timing
python3 timing_setup.py
```

Or manually follow the steps in [Manual Installation](#manual-installation).

## Architecture
```
Timing.app (automatic tracking)
     │
     ▼ (manual or automated CSV export)
┌─────────────────────────────────────────────────────┐
│  timing_fetcher.py                                  │
│  - Parses Advanced CSV exports                      │
│  - Stores in SQLite cache                           │
│  - Generates daily summaries                        │
└─────────────────────────────────────────────────────┘
     │
     ├──▶ git_correlate.py (commits ↔ hours)
     ├──▶ writing_analysis.py (peak writing hours)
     ├──▶ reading_analysis.py (research throughput)
     ├──▶ weekly_digest.py (summaries + notifications)
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  observatory_integration.py                         │
│  - Syncs to Observatory database                    │
│  - Enables unified dashboard queries                │
└─────────────────────────────────────────────────────┘
```

## File Structure

After installation:
```
~/Local/virens/user1/
├── scripts/timing/
│   ├── timing_fetcher.py          # CSV import and caching
│   ├── git_correlate.py           # Git commit correlation
│   ├── weekly_digest.py           # Weekly summaries
│   ├── observatory_integration.py # Observatory sync
│   ├── writing_analysis.py        # Writing pattern analysis
│   ├── reading_analysis.py        # Reading pattern analysis
│   └── README.md                  # Your personal configuration notes
├── data/timing/
│   ├── timing_cache.db            # SQLite cache
│   └── *.csv                      # Timing exports (optional storage)
├── reports/timing/
│   ├── git_correlation_*.md       # Git reports
│   ├── weekly_digest_*.md         # Weekly digests
│   ├── writing_analysis_*.md      # Writing reports
│   └── reading_analysis_*.md      # Reading reports
└── logs/
    ├── timing_daily.log           # Daily sync logs
    └── timing_weekly.log          # Weekly digest logs

~/Library/LaunchAgents/
├── com.virens.timing.daily.plist  # Daily 6:30 AM sync
└── com.virens.timing.weekly.plist # Sunday 6:00 PM digest
```

## Timing.app Configuration

### Export Format Requirements

This integration requires **Advanced CSV** exports from Timing:

1. Open Timing.app
2. Go to **Reports** → select date range
3. Click **Export** → **Advanced**
4. Choose **CSV** format
5. Save to `~/Local/virens/user1/data/timing/`

### CSV Columns Expected

The scripts expect these columns (Timing 2026.1 default Advanced export):

| Column | Description |
|--------|-------------|
| `Project` | Leaf-level project name |
| `Date` | ISO date (YYYY-MM-DD) |
| `Hour` | Hour bucket (ISO timestamp) |
| `Duration` | Seconds in that hour bucket |
| `Application` | App name |
| `Window Title` | Window/document title |

**Note:** Timing exports leaf-level project names only, not full hierarchy paths. The analysis scripts use keyword matching to aggregate into categories.

### Recommended Rule Structure

Timing's power comes from automatic categorization via rules. We recommend a hierarchical project structure:
```
VIRENS (top-level)
├── Development
│   ├── Coding
│   ├── Documentation
│   └── LLM Sessions
├── Research Workflow
│   ├── PDF Reading
│   ├── Book Reading
│   ├── Literature Notes
│   └── Zettelkasten
└── Infrastructure
    ├── Configuration
    └── Maintenance

Research (top-level)
├── Writing
│   ├── Article Drafts
│   ├── Chapter Drafts
│   └── Grant Writing
├── Reading
│   ├── Online Research
│   └── Annotation
└── Citation Management
    └── Bookends

Teaching (top-level)
├── Course Prep
├── Grading
└── Office Hours

Administrative (top-level)
├── Email
├── Meetings
└── Service
```

### Rule Examples

Create rules in Timing.app (Preferences → Rules) that match:

| Rule Name | Match Condition | Project Assignment |
|-----------|-----------------|-------------------|
| Claude AI | App is "Claude" | VIRENS > Development > LLM Sessions |
| Obsidian | App is "Obsidian" | Research > Writing > Zettelkasten |
| DEVONthink | App is "DEVONthink" | Research > Reading > PDF Reading |
| Scrivener | App is "Scrivener" | Research > Writing > Article Drafts |
| Bookends | App is "Bookends" | Research > Citation Management |
| Terminal Dev | App is "Terminal" AND title contains "virens" | VIRENS > Development > Coding |
| Safari Research | App is "Safari" AND title contains "scholar\|jstor\|pdf" | Research > Reading > Online Research |

**Tip:** Start with 10-15 broad rules, then refine as you see uncategorized time in Timing's review.

## Scripts Reference

### timing_fetcher.py

Import Timing CSV exports into SQLite cache.
```bash
# Import a CSV file
python3 timing_fetcher.py ~/Downloads/timing_export.csv

# Query recent data
python3 timing_fetcher.py --summary 7
```

**Options:**
- `<csv_path>` - Path to Timing Advanced CSV export
- `--summary N` - Show summary for last N days
- `--project NAME` - Filter by project name

### git_correlate.py

Correlate Timing hours with git commit activity.
```bash
# Quick summary (stdout)
python3 git_correlate.py --days 30

# Generate full report
python3 git_correlate.py --days 30 --report
```

**Options:**
- `--days N` - Analysis period (default: 30)
- `--report` - Generate markdown + CSV reports
- `--repos PATH` - Additional repository paths

**Default repositories scanned:**
- `~/Local/virens/virens`
- `~/Local/virens/user1`

### weekly_digest.py

Generate weekly productivity summaries.
```bash
# Print summary to stdout
python3 weekly_digest.py

# With macOS notification
python3 weekly_digest.py --notify

# Save report files
python3 weekly_digest.py --save

# Both
python3 weekly_digest.py --notify --save
```

**Options:**
- `--notify` - Show macOS notification
- `--save` - Save markdown + JSON reports
- `--weeks N` - Weeks to include (default: 1)

### observatory_integration.py

Sync Timing data to Observatory database.
```bash
# Sync recent data
python3 observatory_integration.py --sync

# Show sync status
python3 observatory_integration.py --status
```

**Options:**
- `--sync` - Sync data to Observatory
- `--status` - Show recent synced data
- `--days N` - Days to sync (default: 30)

### writing_analysis.py

Analyze writing productivity patterns.
```bash
# Analyze last 90 days
python3 writing_analysis.py

# Custom range
python3 writing_analysis.py --days 30

# Generate report
python3 writing_analysis.py --report
```

**Writing keywords detected:**
- Article, Chapter, Draft, Monograph, Writing
- Grant Draft, Documentation Writing
- Zettelkasten, Literature Notes, MOC Development

**Writing applications detected:**
- Scrivener, Word, Pages, iA Writer, Ulysses

### reading_analysis.py

Analyze reading and research patterns.
```bash
# Analyze last 90 days
python3 reading_analysis.py

# Custom range
python3 reading_analysis.py --days 30

# Generate report
python3 reading_analysis.py --report
```

**Reading keywords detected:**
- PDF Reading, Book Reading, Online Research
- Highlights, DEVONthink, Readwise

**Reading applications detected:**
- Preview, PDF Expert, Highlights, Skim (PDF)
- Books, Kindle, Calibre, Libby (ebook)
- Safari, Chrome, Arc (web research)

## Shell Aliases

Add to your shell configuration:
```zsh
# Timing.app integration
alias timing-summary='python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py --summary 7'
alias timing-import='python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py'
alias timing-digest='python3 ~/Local/virens/user1/scripts/timing/weekly_digest.py --save'
alias timing-digest-notify='python3 ~/Local/virens/user1/scripts/timing/weekly_digest.py --notify --save'
alias timing-git='python3 ~/Local/virens/user1/scripts/timing/git_correlate.py --days 30'
alias timing-git-report='python3 ~/Local/virens/user1/scripts/timing/git_correlate.py --days 30 --report'
alias timing-sync='python3 ~/Local/virens/user1/scripts/timing/observatory_integration.py --sync && python3 ~/Local/virens/user1/scripts/timing/observatory_integration.py --status'
alias timing-writing='python3 ~/Local/virens/user1/scripts/timing/writing_analysis.py'
alias timing-reading='python3 ~/Local/virens/user1/scripts/timing/reading_analysis.py'
alias timing-writing-report='python3 ~/Local/virens/user1/scripts/timing/writing_analysis.py --report'
alias timing-reading-report='python3 ~/Local/virens/user1/scripts/timing/reading_analysis.py --report'

# Workflow shortcut
timing-update() {
    if [[ -z "$1" ]]; then
        echo "Usage: timing-update <path-to-csv>"
        return 1
    fi
    echo "Importing Timing data..."
    python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py "$1"
    echo "\nSyncing to Observatory..."
    python3 ~/Local/virens/user1/scripts/timing/observatory_integration.py --sync
    echo "\nSummary:"
    python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py --summary 7
}
```

## Automation

### LaunchAgents

Two LaunchAgents automate daily sync and weekly digests:

**Daily sync** (`com.virens.timing.daily.plist`):
- Runs: 6:30 AM daily
- Action: Syncs cached data to Observatory
- Log: `~/Local/virens/user1/logs/timing_daily.log`

**Weekly digest** (`com.virens.timing.weekly.plist`):
- Runs: Sunday 6:00 PM
- Action: Generates digest + macOS notification
- Log: `~/Local/virens/user1/logs/timing_weekly.log`

### Automated CSV Export

Timing.app doesn't support scriptable exports in version 2026.1. Options:

1. **Manual export** - Export weekly as part of your review routine
2. **Keyboard Maestro** - Create a macro that navigates Timing's UI to export
3. **Timing URL scheme** - Check future versions for `timing://export` support

Recommended workflow:
- Export manually after significant work sessions
- Export weekly on Sunday before the digest runs

## Customization

### Modifying Keywords

Edit the keyword lists in each analysis script:

**writing_analysis.py:**
```python
WRITING_KEYWORDS = [
    'Article', 'Chapter', 'Draft', 'Monograph', 'Writing',
    # Add your project names here
]
```

**reading_analysis.py:**
```python
READING_KEYWORDS = [
    'PDF Reading', 'Book Reading', 'Online Research',
    # Add your project names here
]
```

### Adding Repositories to Git Correlation

Edit `git_correlate.py`:
```python
DEFAULT_REPOS = [
    Path.home() / "Local/virens/virens",
    Path.home() / "Local/virens/user1",
    # Add more repositories here
]
```

### Changing Automation Schedule

Edit the LaunchAgent plists:
```xml
<!-- Change hour (24h format) -->
<key>Hour</key>
<integer>6</integer>

<!-- Change minute -->
<key>Minute</key>
<integer>30</integer>

<!-- For weekly: 0=Sunday, 1=Monday, etc. -->
<key>Weekday</key>
<integer>0</integer>
```

After editing, reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.virens.timing.daily.plist
launchctl load ~/Library/LaunchAgents/com.virens.timing.daily.plist
```

## Troubleshooting

### "No entries found" in analysis

1. Verify data was imported: `timing-summary`
2. Check keyword matching - your Timing project names may differ
3. Run with `--days 7` to check recent data specifically

### Observatory sync fails

1. Verify Observatory database exists: `ls ~/Local/virens/user1/data/observatory.db`
2. Check the `timing_productivity` table was created
3. Run setup again: `python3 observatory_integration.py --sync`

### LaunchAgent not running
```bash
# Check if loaded
launchctl list | grep virens.timing

# View logs
cat ~/Local/virens/user1/logs/timing_daily.log

# Manual test
launchctl start com.virens.timing.daily
```

### CSV import errors

1. Ensure you're using **Advanced** export (not Simple)
2. Check CSV has expected columns: Project, Date, Hour, Duration
3. Verify date format is ISO (YYYY-MM-DD)

## Manual Installation

If not using `timing_setup.py`:
```bash
# 1. Create directories
mkdir -p ~/Local/virens/user1/scripts/timing
mkdir -p ~/Local/virens/user1/data/timing
mkdir -p ~/Local/virens/user1/reports/timing
mkdir -p ~/Local/virens/user1/logs

# 2. Copy scripts from framework (or create manually)
# Scripts should be placed in ~/Local/virens/user1/scripts/timing/

# 3. Make executable
chmod +x ~/Local/virens/user1/scripts/timing/*.py

# 4. Initialize database (run any script once)
python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py --summary 1

# 5. Install LaunchAgents
cp com.virens.timing.*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.virens.timing.daily.plist
launchctl load ~/Library/LaunchAgents/com.virens.timing.weekly.plist

# 6. Add aliases to shell config
# Append aliases from this README to ~/.zshrc or your aliases file
```

## Data Privacy

- All data stays local on your machine
- No cloud sync or external API calls
- SQLite databases are plain files you control
- Timing.app's own sync (if enabled) is separate from this integration

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01 | Initial release |

---

*Part of the [VIRENS](https://github.com/preterite/virens) academic research workflow system.*
