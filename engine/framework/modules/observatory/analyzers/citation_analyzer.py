#!/usr/bin/env python3
"""
Citation Analyzer - Weekly citation pattern analysis
Focuses on citation velocity and burst detection
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class CitationAnalyzer:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_data = data_dir / "raw"
        self.processed_data = data_dir / "processed"
        self.cache_dir = data_dir / "analysis_cache"
        
        # Ensure directories exist
        for directory in [self.raw_data, self.processed_data, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def analyze_citations(self) -> Dict:
        """Main weekly citation analysis"""
        citations_file = self.raw_data / "citations.json"
        
        if not citations_file.exists():
                analysis = self._empty_analysis()
                self._save_analysis(analysis, 'citation_analysis')
                return analysis
        
        with open(citations_file) as f:
            data = json.load(f)
        
        # Convert to pandas for analysis
        df = pd.DataFrame(data.get('citations', []))
        
        if df.empty:
            analysis = self._empty_analysis()
            self._save_analysis(analysis, 'citation_analysis')
            return analysis

        # Calculate metrics
        total_citations = len(df)
        
        # Citation velocity (last 7 days vs previous 7 days)
        now = datetime.now()
        last_week = now - timedelta(days=7)
        prev_week = now - timedelta(days=14)
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        recent_citations = len(df[df['date'] >= last_week])
        previous_citations = len(df[(df['date'] >= prev_week) & (df['date'] < last_week)])
        
        velocity = recent_citations - previous_citations
        
        # Detect citation bursts
        burst_detected, burst_paper = self._detect_citation_burst(df)
        
        # H-index calculation — load papers.json separately
        papers_file = self.raw_data / "papers.json"
        papers_data = []
        if papers_file.exists():
            with open(papers_file) as pf:
                papers_data = json.load(pf)
                # papers.json is a list of paper dicts with citation_count key
                # _calculate_h_index expects dicts with 'citations' key, so remap
                papers_data = [{'citations': p.get('citation_count', 0)} for p in papers_data]
        h_index = self._calculate_h_index(papers_data)
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'total_citations': total_citations,
            'recent_citations': recent_citations,
            'citation_velocity': velocity,
            'velocity_trend': 'increasing' if velocity > 0 else 'stable' if velocity == 0 else 'decreasing',
            'h_index': h_index,
            'burst_detected': burst_detected,
            'burst_paper': burst_paper,
            'alert_threshold_crossed': burst_detected  # Only alert on bursts
        }

        print("DEBUG: About to save analysis...")
        
        # Cache the analysis
        self._save_analysis(analysis, 'citation_analysis')
        
        return analysis
    
    def _detect_citation_burst(self, df: pd.DataFrame, threshold: int = 5) -> tuple:
        """
        Detect if any paper has received unusually high citations recently
        Returns (burst_detected: bool, paper_title: str or None)
        """
        if df.empty or 'paper_id' not in df.columns:
            return False, None
        
        # Count citations per paper in last 7 days
        now = datetime.now()
        last_week = now - timedelta(days=7)
        recent_df = df[df['date'] >= last_week]
        
        if recent_df.empty:
            return False, None
        
        paper_counts = recent_df.groupby('paper_id').size()
        
        # Check if any paper exceeds threshold
        if paper_counts.max() >= threshold:
            burst_paper_id = paper_counts.idxmax()
            burst_paper_title = df[df['paper_id'] == burst_paper_id]['paper_title'].iloc[0]
            return True, burst_paper_title
        
        return False, None
    
    def _calculate_h_index(self, papers: List[Dict]) -> int:
        """Calculate h-index from papers list"""
        if not papers:
            return 0
        
        citation_counts = sorted([p.get('citations', 0) for p in papers], reverse=True)
        
        h = 0
        for i, citations in enumerate(citation_counts, 1):
            if citations >= i:
                h = i
            else:
                break
        
        return h
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_citations': 0,
            'recent_citations': 0,
            'citation_velocity': 0,
            'velocity_trend': 'no_data',
            'h_index': 0,
            'burst_detected': False,
            'burst_paper': None,
            'alert_threshold_crossed': False
        }
    
    def _save_analysis(self, analysis: Dict, analysis_type: str):
        """Save analysis results with timestamp"""
        try:
            # Ensure directory exists
            self.processed_data.mkdir(parents=True, exist_ok=True)
            
            filename = f"{analysis_type}_{datetime.now().strftime('%Y%m%d')}.json"
            output_file = self.processed_data / filename
            
            print(f"Attempting to save: {output_file}")
            
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            print(f"✅ Saved: {output_file}")
            
            # Also save as "latest"
            latest_file = self.processed_data / f"{analysis_type}_latest.json"
            with open(latest_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            print(f"✅ Saved: {latest_file}")
            
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'))
    from core.config import config
    data_dir = config.observatory_data
    analyzer = CitationAnalyzer(data_dir)
    results = analyzer.analyze_citations()
    print(json.dumps(results, indent=2))
