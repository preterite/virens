#!/usr/bin/env python3
"""
Trend Analyzer - Monthly field and keyword monitoring
Tracks your specific journals and research domains
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set
from collections import Counter

class TrendAnalyzer:
    # Your monitored journals
    JOURNALS = {
        'College English': '0010-0994',
        'College Composition and Communication': '0010-096X',
        'Kairos': '1521-2300',
        'Computers and Composition': '1873-2011',
        'Rhetoric Review': '1532-7981',
        'Rhetoric Society Quarterly': '1930-322X',
        'Digital Humanities Quarterly': '1938-4122'
    }
    
    # Your research keywords
    KEYWORDS = [
        'rhetoric', 'composition', 'rhetoric and composition', 'writing studies',
        'digital humanities', 'political economy', 'critical theory',
        'economics Marxian', 'economics heterodox', 'economics Marxist',
        'cultural studies', 'digital rhetoric', 'computers and writing',
        'computers and composition', 'Marx', 'postcapitalism', 'postcapitalist',
        'labor', 'capital', 'intellectual property', 'reading',
        'LLM', 'cognitive psychology', 'poetics', 'necropolitics', 'surveillance'
    ]
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_data = data_dir / "raw"
        self.processed_data = data_dir / "processed"
    
    def analyze_trends(self) -> Dict:
        """Monthly trend analysis"""
        papers_file = self.raw_data / "field_papers.json"

        if not papers_file.exists():
            analysis = self._empty_analysis()
            self._save_analysis(analysis, 'trend_analysis')
            return self._empty_analysis()
        
        with open(papers_file) as f:
            papers = json.load(f)
        
        # Analyze by journal
        journal_activity = self._analyze_journal_activity(papers)
        
        # Analyze keywords
        keyword_trends = self._analyze_keywords(papers)
        
        # Emerging topics
        emerging = self._identify_emerging_topics(papers)
        
        # Top relevant papers sorted by relevance score
        top_papers = sorted(papers, key=lambda p: p.get('relevance_score', 0), reverse=True)[:5]
        top_relevant = [
            {
                'title': p.get('title', ''),
                'journal': p.get('journal', ''),
                'year': p.get('year'),
                'matched_keywords': p.get('matched_keywords', []),
                'relevance_score': p.get('relevance_score', 0)
            }
            for p in top_papers
        ]

        analysis = {
            'timestamp': datetime.now().isoformat(),
            'period': 'monthly',
            'journal_activity': journal_activity,
            'keyword_trends': keyword_trends,
            'emerging_topics': emerging,
            'total_papers_monitored': len(papers),
            'top_relevant_papers': top_relevant
        }
        
        self._save_analysis(analysis, 'trend_analysis')
        
        return analysis
    
    def _analyze_journal_activity(self, papers: List[Dict]) -> Dict:
        """Count papers per monitored journal"""
        activity = {journal: 0 for journal in self.JOURNALS.keys()}
        
        for paper in papers:
            journal = paper.get('journal', '')
            if journal in activity:
                activity[journal] += 1
        
        return activity
    
    def _analyze_keywords(self, papers: List[Dict]) -> Dict:
        """Track occurrence of your research keywords"""
        keyword_counts = Counter()
        
        for paper in papers:
            # Check title and abstract
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
            
            for keyword in self.KEYWORDS:
                if keyword.lower() in text:
                    keyword_counts[keyword] += 1
        
        # Return top 10 most frequent
        return dict(keyword_counts.most_common(10))
    
    def _identify_emerging_topics(self, papers: List[Dict]) -> List[str]:
        """
        Identify topics that are appearing more frequently
        compared to previous month
        """
        # This is simplified - in production, you'd compare to historical data
        recent_papers = [p for p in papers 
                        if self._is_recent(p.get('date', ''))]
        
        if not recent_papers:
            return []
        
        # Extract common phrases (simplified)
        emerging = []
        for paper in recent_papers[:5]:  # Top 5 recent papers
            title = paper.get('title', '')
            if any(kw in title.lower() for kw in ['ai', 'llm', 'generative']):
                emerging.append(title)
        
        return emerging
    
    def _is_recent(self, date_str: str, days: int = 30) -> bool:
        """Check if date is within last N days"""
        try:
            date = datetime.fromisoformat(date_str)
            return (datetime.now() - date).days <= days
        except:
            return False
    
    def _empty_analysis(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'period': 'monthly',
            'journal_activity': {j: 0 for j in self.JOURNALS.keys()},
            'keyword_trends': {},
            'emerging_topics': [],
            'total_papers_monitored': 0
        }
    
    def _save_analysis(self, analysis: Dict, analysis_type: str):
        filename = f"{analysis_type}_{datetime.now().strftime('%Y%m')}.json"
        output_file = self.processed_data / filename
        
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        latest_file = self.processed_data / f"{analysis_type}_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(analysis, f, indent=2)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'))
    from core.config import config
    data_dir = config.observatory_data
    analyzer = TrendAnalyzer(data_dir)
    results = analyzer.analyze_trends()
    print(json.dumps(results, indent=2))
