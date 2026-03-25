#!/usr/bin/env python3
"""
Observatory Weekly Reporter
============================
Reads the four *_latest.json analyzer outputs and writes a structured
markdown report to the Scholar vault for the virens-prospector skill.

Output:
  - observatory-report-YYYY-WW.md  (dated archive copy)
  - observatory-report-latest.md   (the file prospector reads on init)

Both written to: ~/Local/virens/user1/Scholar/000_observatory/weekly-reports/
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Wire up config — framework root must come first to shadow user instance's core/
_obs_root = Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'
sys.path.insert(0, str(_obs_root))

import sqlite3
from core.config import config


def load_json(processed_dir: Path, analysis_type: str) -> dict:
    """Load a *_latest.json file; return empty dict if missing."""
    path = processed_dir / f"{analysis_type}_latest.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception as e:
            print(f"⚠️  Could not load {path.name}: {e}")
    return {}


def format_velocity(v: int) -> str:
    if v > 0:
        return f"+{v} (increasing)"
    elif v == 0:
        return "stable"
    else:
        return f"{v} (decreasing)"


def _format_top_papers(papers: list) -> str:
    if not papers:
        return "*(No field papers yet — run fetch_field_papers() to populate)*\n"
    lines = []
    for i, p in enumerate(papers[:5], 1):
        kws = ", ".join(p.get('matched_keywords', [])[:3])
        lines.append(
            f"{i}. **{p['title']}** — {p.get('authors', '')}. _{p.get('journal', '?')}_ ({p.get('year', '?')})"
            f"  \n   Keywords matched: {kws or 'n/a'}"
        )
    return "\n".join(lines) + "\n"


def load_github_metrics() -> dict:
    """Query external_metrics table for GitHub data."""
    db_path = config.database_path
    if not db_path.exists():
        return {}
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT metric_name, metric_value, metadata, fetched_at
            FROM external_metrics
            WHERE source = 'github'
            ORDER BY fetched_at DESC
        ''')
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()

        if not rows:
            return {}

        # Build a dict of latest value per metric_name
        metrics = {}
        seen = set()
        for row in rows:
            name = row['metric_name']
            if name not in seen:
                seen.add(name)
                metrics[name] = row['metric_value']
                if row.get('metadata'):
                    try:
                        metrics[f"{name}_meta"] = json.loads(row['metadata'])
                    except (json.JSONDecodeError, TypeError):
                        pass

        # Also get commit count in last 90 days
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=90)).isoformat()
        cursor2 = sqlite3.connect(db_path).cursor()
        cursor2.execute('''
            SELECT COUNT(*) FROM external_metrics
            WHERE source = 'github' AND metric_name = 'commit'
            AND fetched_at >= ?
        ''', (cutoff,))
        count_row = cursor2.fetchone()
        metrics['commits_90d'] = count_row[0] if count_row else 0
        cursor2.connection.close()

        # Get distinct repos
        cursor3 = sqlite3.connect(db_path).cursor()
        cursor3.execute('''
            SELECT DISTINCT metric_value FROM external_metrics
            WHERE source = 'github' AND metric_name = 'active_repo'
        ''')
        repos = [r[0] for r in cursor3.fetchall()]
        metrics['active_repos'] = repos
        cursor3.connection.close()

        return metrics
    except Exception as e:
        print(f"⚠️  Could not load GitHub metrics: {e}")
        return {}


def _format_github_section(github: Optional[dict]) -> str:
    if not github:
        return "*(No GitHub data in external_metrics table)*"
    lines = []
    commits_90d = github.get('commits_90d', 0)
    lines.append(f"- Commits (last 90 days): {commits_90d}")
    active_repos = github.get('active_repos', [])
    if active_repos:
        lines.append(f"- Active repositories: {', '.join(active_repos)}")
    else:
        lines.append("- Active repositories: (none tracked)")
    # Include any other metrics present
    skip = {'commits_90d', 'active_repos'}
    for key, val in github.items():
        if key in skip or key.endswith('_meta'):
            continue
        lines.append(f"- {key}: {val}")
    return "\n".join(lines)


def build_report(citation: dict, network: dict, trend: dict, teaching: dict,
                  github: Optional[dict] = None) -> str:
    now = datetime.now()
    week_str = now.strftime('%Y-W%W')
    date_str = now.strftime('%Y-%m-%d')

    # --- Publication Metrics ---
    total_pubs   = citation.get('total_citations', 0)  # total tracked citations
    h_index      = citation.get('h_index', 0)
    total_cites  = citation.get('total_citations', 0)
    velocity     = citation.get('citation_velocity', 0)
    vel_trend    = citation.get('velocity_trend', 'no_data')
    burst        = citation.get('burst_detected', False)
    burst_paper  = citation.get('burst_paper', None)

    burst_line = "no"
    if burst and burst_paper:
        burst_line = f"yes — {burst_paper}"

    # --- Field Activity ---
    journal_activity = trend.get('journal_activity', {})
    journal_rows = ""
    for journal, count in journal_activity.items():
        journal_rows += f"| {journal} | {count} |\n"
    if not journal_rows:
        journal_rows = "| (field_papers pipeline not yet populated) | — |\n"

    # --- Keyword Activity ---
    keyword_trends = trend.get('keyword_trends', {})
    keyword_lines = ""
    for kw, count in list(keyword_trends.items())[:10]:
        keyword_lines += f"- {kw}: {count} occurrences\n"
    if not keyword_lines:
        keyword_lines = "- (field_papers pipeline not yet populated)\n"

    total_monitored = trend.get('total_papers_monitored', 0)

    # --- Top Recent Field Papers ---
    top_papers = trend.get('top_relevant_papers', [])

    # --- Teaching ---
    dist = teaching.get('course_distribution', {})
    compliance = teaching.get('contract_compliance', {})
    total_courses     = dist.get('total_courses', 0)
    e101_count        = dist.get('english_101_count', 0)
    grad_count        = dist.get('graduate_seminar_count', 0)
    other_count       = dist.get('other_undergrad_count', 0)
    overall_compliant = compliance.get('overall_compliant', True)
    service_alert     = compliance.get('service_equity_alert', False)
    recommendations   = teaching.get('recommendations', [])

    compliance_str = "compliant" if overall_compliant else "overload detected"
    service_str    = "service equity alert" if service_alert else "none"

    rec_lines = "\n".join(f"- {r}" for r in recommendations) if recommendations else "- None"

    # --- Network ---
    total_collabs = network.get('total_collaborators', 0)
    net_metrics   = network.get('network_metrics', {})
    density       = net_metrics.get('network_density', 'n/a')
    clustering    = net_metrics.get('clustering_coefficient', 'n/a')

    strategic = network.get('strategic_collaborators', [])
    collab_lines = ""
    for c in strategic[:5]:
        collab_lines += f"- {c['name']} (centrality: {c['centrality_score']}, collabs: {c['collaboration_count']})\n"
    if not collab_lines:
        collab_lines = "- (no collaboration data yet)\n"

    # --- Data freshness ---
    cite_ts    = citation.get('timestamp', 'unknown')[:10]
    trend_ts   = trend.get('timestamp', 'not yet populated')
    if trend_ts and trend_ts != 'not yet populated':
        trend_ts = trend_ts[:10]
    network_ts = network.get('timestamp', 'unknown')[:10]

    report = f"""---
generated: {date_str}
week: {week_str}
observatory-version: 1.0
---

# Observatory Weekly Report: Week {week_str}

## Publication Metrics
- Total citations tracked: {total_cites}
- h-index (OpenAlex): {h_index}
- Citation velocity (last 7 days vs. prior 7): {format_velocity(velocity)}
- Velocity trend: {vel_trend}
- Citation burst detected: {burst_line}

## Collaboration Network
- Total collaborators: {total_collabs}
- Network density: {density}
- Clustering coefficient: {clustering}

Top collaborators by centrality:
{collab_lines}
## Field Activity (last 90 days)
Total papers monitored: {total_monitored}

| Journal | New Papers |
|---------|------------|
{journal_rows}
## Top Relevant Recent Papers (last 90 days)
{_format_top_papers(top_papers)}

## Keyword Activity
Top keywords in monitored field (last 90 days):
{keyword_lines}
## Teaching Load
- Total courses on record: {total_courses}
- English 101 sections: {e101_count}
- Graduate seminars: {grad_count}
- Other undergraduate: {other_count}
- Contract compliance: {compliance_str}
- Service equity alert: {service_str}

Teaching recommendations:
{rec_lines}

## GitHub Activity
{_format_github_section(github)}

## Similar Researchers
*(Populated after Session 2 — find_similar_researchers(), Item 12e)*

## Data Freshness
- Citation data last updated: {cite_ts}
- Field papers last updated: {trend_ts}
- Network analysis last updated: {network_ts}
"""
    return report


def main():
    processed_dir = config.observatory_data / 'processed'
    vault_reports = (
        Path.home() / 'Local/virens/user1/Scholar/000_observatory/weekly-reports'
    )
    vault_reports.mkdir(parents=True, exist_ok=True)

    print("Observatory Weekly Reporter")
    print(f"   Reading from: {processed_dir}")
    print(f"   Writing to:   {vault_reports}")

    # Load analyzer outputs
    citation = load_json(processed_dir, 'citation_analysis')
    network  = load_json(processed_dir, 'network_analysis')
    trend    = load_json(processed_dir, 'trend_analysis')
    teaching = load_json(processed_dir, 'teaching_analysis')

    # Load GitHub metrics from DB
    github = load_github_metrics()

    # Build report
    report = build_report(citation, network, trend, teaching, github=github)

    # Write dated archive copy
    week_str  = datetime.now().strftime('%Y-W%W')
    dated_path = vault_reports / f"observatory-report-{week_str}.md"
    dated_path.write_text(report)
    print(f"   Written: {dated_path.name}")

    # Write/overwrite latest (what the prospector reads)
    latest_path = vault_reports / "observatory-report-latest.md"
    latest_path.write_text(report)
    print(f"   Written: {latest_path.name}")

    print("   Done.")


if __name__ == '__main__':
    main()
