#!/usr/bin/env python3
"""
timing_setup.py - Automated setup for VIRENS Timing.app integration

Creates directories, initializes databases, installs scripts,
configures LaunchAgents, and adds shell aliases.

Usage:
    python3 timing_setup.py           # Interactive setup
    python3 timing_setup.py --all     # Non-interactive, install everything
    python3 timing_setup.py --check   # Check current installation status
"""

import os
import sys
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

VIRENS_USER_DIR = Path.home() / "Local/virens/user1"
FRAMEWORK_DIR = Path.home() / "Local/virens/virens/engine/framework/modules/timing"
LAUNCHAGENTS_DIR = Path.home() / "Library/LaunchAgents"

DIRECTORIES = [
    VIRENS_USER_DIR / "scripts/timing",
    VIRENS_USER_DIR / "data/timing",
    VIRENS_USER_DIR / "reports/timing",
    VIRENS_USER_DIR / "logs",
]

SCRIPTS = [
    "timing_fetcher.py",
    "git_correlate.py",
    "weekly_digest.py",
    "observatory_integration.py",
    "writing_analysis.py",
    "reading_analysis.py",
]

ALIASES = '''
# ============================================================================
# Timing.app Integration (added by timing_setup.py)
# ============================================================================

# Import and sync
alias timing-summary='python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py --summary 7'
alias timing-import='python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py'
alias timing-digest='python3 ~/Local/virens/user1/scripts/timing/weekly_digest.py --save'
alias timing-digest-notify='python3 ~/Local/virens/user1/scripts/timing/weekly_digest.py --notify --save'

# Git correlation
alias timing-git='python3 ~/Local/virens/user1/scripts/timing/git_correlate.py --days 30'
alias timing-git-report='python3 ~/Local/virens/user1/scripts/timing/git_correlate.py --days 30 --report'

# Observatory integration
alias timing-sync='python3 ~/Local/virens/user1/scripts/timing/observatory_integration.py --sync && python3 ~/Local/virens/user1/scripts/timing/observatory_integration.py --status'

# Productivity analysis
alias timing-writing='python3 ~/Local/virens/user1/scripts/timing/writing_analysis.py'
alias timing-reading='python3 ~/Local/virens/user1/scripts/timing/reading_analysis.py'
alias timing-writing-report='python3 ~/Local/virens/user1/scripts/timing/writing_analysis.py --report'
alias timing-reading-report='python3 ~/Local/virens/user1/scripts/timing/reading_analysis.py --report'

# Workflow function
timing-update() {
    if [[ -z "$1" ]]; then
        echo "Usage: timing-update <path-to-csv>"
        return 1
    fi
    echo "Importing Timing data..."
    python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py "$1"
    echo "\\nSyncing to Observatory..."
    python3 ~/Local/virens/user1/scripts/timing/observatory_integration.py --sync
    echo "\\nSummary:"
    python3 ~/Local/virens/user1/scripts/timing/timing_fetcher.py --summary 7
}
'''

DAILY_LAUNCHAGENT = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.virens.timing.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{scripts_dir}/observatory_integration.py</string>
        <string>--sync</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{logs_dir}/timing_daily.log</string>
    <key>StandardErrorPath</key>
    <string>{logs_dir}/timing_daily.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
'''

WEEKLY_LAUNCHAGENT = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.virens.timing.weekly</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{scripts_dir}/weekly_digest.py</string>
        <string>--notify</string>
        <string>--save</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{logs_dir}/timing_weekly.log</string>
    <key>StandardErrorPath</key>
    <string>{logs_dir}/timing_weekly.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
'''

TIMING_CACHE_SCHEMA = '''
CREATE TABLE IF NOT EXISTS time_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT,
    start_time TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    application TEXT,
    window_title TEXT,
    imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project, start_time, duration_seconds)
);

CREATE TABLE IF NOT EXISTS daily_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    project TEXT,
    total_seconds INTEGER NOT NULL,
    entry_count INTEGER DEFAULT 1,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, project)
);

CREATE TABLE IF NOT EXISTS weekly_digests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start TEXT NOT NULL,
    week_end TEXT NOT NULL,
    total_hours REAL,
    category_breakdown TEXT,
    git_commits INTEGER,
    notes_created INTEGER,
    generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(week_start)
);

CREATE INDEX IF NOT EXISTS idx_entries_start ON time_entries(start_time);
CREATE INDEX IF NOT EXISTS idx_entries_project ON time_entries(project);
CREATE INDEX IF NOT EXISTS idx_summary_date ON daily_summary(date);
'''

OBSERVATORY_TIMING_SCHEMA = '''
CREATE TABLE IF NOT EXISTS timing_productivity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    metric_type TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value REAL NOT NULL,
    metadata TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, metric_type, metric_name)
);

CREATE INDEX IF NOT EXISTS idx_timing_prod_date ON timing_productivity(date);
CREATE INDEX IF NOT EXISTS idx_timing_prod_type ON timing_productivity(metric_type);
'''

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def print_status(item, status, note=""):
    """Print a status line."""
    symbol = "✅" if status else "❌"
    note_str = f" ({note})" if note else ""
    print(f"  {symbol} {item}{note_str}")

def prompt_yes_no(question, default=True):
    """Prompt for yes/no response."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{question} [{default_str}]: ").strip().lower()
    if not response:
        return default
    return response in ('y', 'yes')

def run_command(cmd):
    """Run a shell command and return success status."""
    return os.system(cmd) == 0

# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

def check_prerequisites():
    """Check that prerequisites are met."""
    print_header("Checking Prerequisites")
    
    all_good = True
    
    # Check VIRENS user directory
    if VIRENS_USER_DIR.exists():
        print_status("VIRENS user directory", True, str(VIRENS_USER_DIR))
    else:
        print_status("VIRENS user directory", False, "not found")
        all_good = False
    
    # Check Python version
    py_version = sys.version_info
    if py_version >= (3, 9):
        print_status("Python version", True, f"{py_version.major}.{py_version.minor}")
    else:
        print_status("Python version", False, f"{py_version.major}.{py_version.minor} (need 3.9+)")
        all_good = False
    
    # Check Observatory database
    obs_db = VIRENS_USER_DIR / "data/observatory.db"
    if obs_db.exists():
        print_status("Observatory database", True, str(obs_db))
    else:
        print_status("Observatory database", False, "not found - will create timing tables separately")
    
    # Check Timing.app
    timing_app = Path("/Applications/Timing.app")
    if timing_app.exists():
        print_status("Timing.app", True, "installed")
    else:
        print_status("Timing.app", False, "not found in /Applications")
        print("         Note: Timing.app is required but scripts will still install")
    
    return all_good

def create_directories():
    """Create required directories."""
    print_header("Creating Directories")
    
    for dir_path in DIRECTORIES:
        if dir_path.exists():
            print_status(str(dir_path.relative_to(Path.home())), True, "exists")
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            print_status(str(dir_path.relative_to(Path.home())), True, "created")

def initialize_databases():
    """Initialize SQLite databases."""
    print_header("Initializing Databases")
    
    # Timing cache database
    cache_db = VIRENS_USER_DIR / "data/timing/timing_cache.db"
    try:
        conn = sqlite3.connect(cache_db)
        conn.executescript(TIMING_CACHE_SCHEMA)
        conn.commit()
        conn.close()
        print_status("timing_cache.db", True, "initialized")
    except Exception as e:
        print_status("timing_cache.db", False, str(e))
    
    # Observatory timing table
    obs_db = VIRENS_USER_DIR / "data/observatory.db"
    if obs_db.exists():
        try:
            conn = sqlite3.connect(obs_db)
            conn.executescript(OBSERVATORY_TIMING_SCHEMA)
            conn.commit()
            conn.close()
            print_status("observatory.db timing_productivity table", True, "initialized")
        except Exception as e:
            print_status("observatory.db timing_productivity table", False, str(e))
    else:
        print_status("observatory.db", False, "skipped - database doesn't exist")

def check_scripts_source():
    """Check if scripts exist in user directory or need to be noted."""
    scripts_dir = VIRENS_USER_DIR / "scripts/timing"
    
    existing = []
    missing = []
    
    for script in SCRIPTS:
        if (scripts_dir / script).exists():
            existing.append(script)
        else:
            missing.append(script)
    
    return existing, missing

def install_scripts_note():
    """Print note about script installation."""
    print_header("Scripts Installation")
    
    scripts_dir = VIRENS_USER_DIR / "scripts/timing"
    existing, missing = check_scripts_source()
    
    if existing:
        print(f"\n  Already installed ({len(existing)}):")
        for script in existing:
            print_status(script, True)
    
    if missing:
        print(f"\n  Missing ({len(missing)}):")
        for script in missing:
            print_status(script, False)
        
        print("\n  To install missing scripts, copy them from your current session")
        print("  or recreate from the framework README templates.")
        print(f"\n  Target directory: {scripts_dir}")
    
    # Make existing scripts executable
    for script in existing:
        script_path = scripts_dir / script
        script_path.chmod(0o755)

def install_launchagents(interactive=True):
    """Install LaunchAgent plist files."""
    print_header("Installing LaunchAgents")
    
    scripts_dir = VIRENS_USER_DIR / "scripts/timing"
    logs_dir = VIRENS_USER_DIR / "logs"
    
    agents = [
        ("com.virens.timing.daily.plist", DAILY_LAUNCHAGENT),
        ("com.virens.timing.weekly.plist", WEEKLY_LAUNCHAGENT),
    ]
    
    for filename, template in agents:
        plist_path = LAUNCHAGENTS_DIR / filename
        
        if plist_path.exists():
            print_status(filename, True, "already exists")
            continue
        
        if interactive:
            if not prompt_yes_no(f"  Install {filename}?"):
                print_status(filename, False, "skipped")
                continue
        
        # Generate plist content
        content = template.format(
            scripts_dir=scripts_dir,
            logs_dir=logs_dir
        )
        
        try:
            with open(plist_path, 'w') as f:
                f.write(content)
            print_status(filename, True, "created")
            
            # Load the agent
            if run_command(f'launchctl load "{plist_path}" 2>/dev/null'):
                print(f"         Loaded into launchctl")
            else:
                print(f"         Note: Load manually with: launchctl load \"{plist_path}\"")
        except Exception as e:
            print_status(filename, False, str(e))

def install_aliases(interactive=True):
    """Add aliases to user's shell configuration."""
    print_header("Installing Shell Aliases")
    
    aliases_file = VIRENS_USER_DIR / "dotfiles/aliases.zsh"
    
    # Check if aliases already exist
    if aliases_file.exists():
        content = aliases_file.read_text()
        if "timing-summary" in content:
            print_status("Timing aliases", True, "already installed")
            return
    
    if interactive:
        if not prompt_yes_no(f"  Add Timing aliases to {aliases_file}?"):
            print_status("Timing aliases", False, "skipped")
            return
    
    try:
        # Append aliases
        with open(aliases_file, 'a') as f:
            f.write("\n" + ALIASES)
        print_status("Timing aliases", True, f"added to {aliases_file.name}")
        print("\n  Run to activate: source ~/.zshrc")
        print("  Or: source ~/Local/virens/user1/dotfiles/aliases.zsh")
    except Exception as e:
        print_status("Timing aliases", False, str(e))

def print_timing_setup_guide():
    """Print guide for Timing.app configuration."""
    print_header("Timing.app Configuration Guide")
    
    print("""
  Timing.app requires manual rule configuration. Here's a quick-start guide:

  1. OPEN TIMING PREFERENCES
     Timing → Preferences → Rules

  2. CREATE APPLICATION RULES (highest priority)
     
     Examples:
     ┌─────────────────┬────────────────────────────────────────┐
     │ App Match       │ Project Assignment                     │
     ├─────────────────┼────────────────────────────────────────┤
     │ Claude          │ VIRENS > Development > LLM Sessions    │
     │ Obsidian        │ VIRENS > Research Workflow > Obsidian  │
     │ DEVONthink 3    │ VIRENS > Research Workflow > DEVONthink│
     │ Scrivener 3     │ Research > Writing > Article Drafts    │
     │ Mail            │ Administrative > Email                 │
     │ Terminal/iTerm  │ VIRENS > Development > Coding          │
     └─────────────────┴────────────────────────────────────────┘

  3. CREATE TITLE RULES (refinement)
     
     Examples:
     ┌─────────────────────────┬─────────────────────────────────┐
     │ Title Contains          │ Project Assignment              │
     ├─────────────────────────┼─────────────────────────────────┤
     │ jstor|scholar.google    │ Research > Reading > Online     │
     │ github.com              │ VIRENS > Development > Coding   │
     │ .pdf                    │ Research > Reading > PDF Reading│
     └─────────────────────────┴─────────────────────────────────┘

  4. CREATE PROJECT HIERARCHY
     
     Recommended top-level categories:
     • VIRENS (development work)
     • Research (scholarship)
     • Teaching (courses, grading)
     • Administrative (email, meetings)

  5. TEST YOUR RULES
     Work for 10-15 minutes, then check Timing's Review tab
     to verify categorization is correct.

  See the full README for detailed rule patterns:
  ~/Local/virens/virens/engine/framework/modules/timing/README.md
""")

def print_next_steps():
    """Print next steps after installation."""
    print_header("Next Steps")
    
    print("""
  1. CONFIGURE TIMING.APP
     Set up rules as described above (if not already done)

  2. SOURCE ALIASES
     source ~/Local/virens/user1/dotfiles/aliases.zsh

  3. EXPORT FROM TIMING
     Timing → Reports → Select Range → Export → Advanced → CSV
     Save to: ~/Local/virens/user1/data/timing/

  4. IMPORT DATA
     timing-update ~/Local/virens/user1/data/timing/your_export.csv

  5. VERIFY
     timing-summary    # Check imported data
     timing-sync       # Verify Observatory integration

  Documentation:
  • Framework README: ~/Local/virens/virens/engine/framework/modules/timing/README.md
  • Personal README:  ~/Local/virens/user1/scripts/timing/README.md
""")

def check_installation():
    """Check current installation status."""
    print_header("Installation Status Check")
    
    # Directories
    print("\n  Directories:")
    for dir_path in DIRECTORIES:
        exists = dir_path.exists()
        print_status(str(dir_path.relative_to(Path.home())), exists)
    
    # Databases
    print("\n  Databases:")
    cache_db = VIRENS_USER_DIR / "data/timing/timing_cache.db"
    print_status("timing_cache.db", cache_db.exists())
    
    obs_db = VIRENS_USER_DIR / "data/observatory.db"
    if obs_db.exists():
        # Check for timing table
        try:
            conn = sqlite3.connect(obs_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timing_productivity'")
            has_table = cursor.fetchone() is not None
            conn.close()
            print_status("timing_productivity table", has_table)
        except:
            print_status("timing_productivity table", False, "error checking")
    else:
        print_status("observatory.db", False, "not found")
    
    # Scripts
    print("\n  Scripts:")
    scripts_dir = VIRENS_USER_DIR / "scripts/timing"
    for script in SCRIPTS:
        script_path = scripts_dir / script
        print_status(script, script_path.exists())
    
    # LaunchAgents
    print("\n  LaunchAgents:")
    for agent in ["com.virens.timing.daily.plist", "com.virens.timing.weekly.plist"]:
        agent_path = LAUNCHAGENTS_DIR / agent
        if agent_path.exists():
            # Check if loaded
            result = os.popen(f'launchctl list | grep "{agent.replace(".plist", "")}"').read()
            loaded = bool(result.strip())
            status_note = "loaded" if loaded else "not loaded"
            print_status(agent, True, status_note)
        else:
            print_status(agent, False)
    
    # Aliases
    print("\n  Aliases:")
    aliases_file = VIRENS_USER_DIR / "dotfiles/aliases.zsh"
    if aliases_file.exists():
        content = aliases_file.read_text()
        has_aliases = "timing-summary" in content
        print_status("Timing aliases in aliases.zsh", has_aliases)
    else:
        print_status("aliases.zsh", False, "file not found")
    
    # Data status
    print("\n  Data Status:")
    if cache_db.exists():
        try:
            conn = sqlite3.connect(cache_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM time_entries")
            entry_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM daily_summary")
            summary_count = cursor.fetchone()[0]
            conn.close()
            print(f"    Time entries: {entry_count}")
            print(f"    Daily summaries: {summary_count}")
        except Exception as e:
            print(f"    Error reading data: {e}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Set up VIRENS Timing.app integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 timing_setup.py           # Interactive setup
  python3 timing_setup.py --all     # Install everything non-interactively
  python3 timing_setup.py --check   # Check installation status
        """
    )
    parser.add_argument("--all", action="store_true",
                       help="Install everything without prompts")
    parser.add_argument("--check", action="store_true",
                       help="Check current installation status")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  VIRENS Timing.app Integration Setup")
    print("="*60)
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  User directory: {VIRENS_USER_DIR}")
    
    if args.check:
        check_installation()
        return
    
    interactive = not args.all
    
    # Run setup steps
    prereqs_ok = check_prerequisites()
    
    if not prereqs_ok and interactive:
        if not prompt_yes_no("\n  Prerequisites not fully met. Continue anyway?", default=False):
            print("\n  Setup cancelled.")
            return
    
    create_directories()
    initialize_databases()
    install_scripts_note()
    install_launchagents(interactive)
    install_aliases(interactive)
    print_timing_setup_guide()
    print_next_steps()
    
    print("\n" + "="*60)
    print("  Setup complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
