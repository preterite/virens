#!/usr/bin/env python3
"""
Network Analyzer - Collaboration pattern analysis
Batch processing for network metrics
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
from collections import defaultdict
import networkx as nx

class NetworkAnalyzer:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_data = data_dir / "raw"
        self.processed_data = data_dir / "processed"
    
    def analyze_network(self) -> Dict:
        """Batch analysis of collaboration network"""
        papers_file = self.raw_data / "papers.json"
        
        if not papers_file.exists():
            analysis = self._empty_analysis()
            self._save_analysis(analysis, 'network_analysis')
            return self._empty_analysis()

        with open(papers_file) as f:
            papers = json.load(f)
        
        # Build collaboration graph
        G = self._build_collaboration_graph(papers)
        
        # Calculate network metrics
        metrics = self._calculate_network_metrics(G)
        
        # Identify strategic collaborators
        strategic = self._identify_strategic_collaborators(G, papers)
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'total_collaborators': len(G.nodes()) - 1,  # Exclude self
            'total_collaborations': G.number_of_edges(),
            'network_metrics': metrics,
            'strategic_collaborators': strategic,
            'collaboration_frequency': self._collaboration_frequency(papers)
        }
        
        self._save_analysis(analysis, 'network_analysis')
        
        return analysis
    
    def _build_collaboration_graph(self, papers: List[Dict]) -> nx.Graph:
        """Build networkx graph from papers"""
        G = nx.Graph()
        
        for paper in papers:
            authors = paper.get('authors', [])
            
            # Add edges between all co-authors
            for i, author1 in enumerate(authors):
                for author2 in authors[i+1:]:
                    if G.has_edge(author1, author2):
                        G[author1][author2]['weight'] += 1
                    else:
                        G.add_edge(author1, author2, weight=1)
        
        return G
    
    def _calculate_network_metrics(self, G: nx.Graph) -> Dict:
        """Calculate key network metrics"""
        if len(G) == 0:
            return {}
        
        try:
            # Density: how connected is your network
            density = nx.density(G)
            
            # Average clustering: how clustered are collaborations
            clustering = nx.average_clustering(G) if len(G) > 1 else 0
            
            return {
                'network_density': round(density, 3),
                'clustering_coefficient': round(clustering, 3),
                'connected_components': nx.number_connected_components(G)
            }
        except:
            return {}
    
    def _identify_strategic_collaborators(self, G: nx.Graph, papers: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Identify collaborators who are:
        1. Frequent co-authors
        2. Well-connected in the field
        3. Associated with high-impact papers
        """
        strategic = []
        
        # Get degree centrality (how connected each person is)
        if len(G) > 0:
            centrality = nx.degree_centrality(G)
            
            # Sort by centrality
            top_collaborators = sorted(centrality.items(), 
                                      key=lambda x: x[1], 
                                      reverse=True)[:top_n]
            
            for name, centrality_score in top_collaborators:
                # Count collaborations with this person
                collab_count = sum(1 for p in papers 
                                  if name in p.get('authors', []))
                
                strategic.append({
                    'name': name,
                    'centrality_score': round(centrality_score, 3),
                    'collaboration_count': collab_count
                })
        
        return strategic
    
    def _collaboration_frequency(self, papers: List[Dict]) -> Dict:
        """Analyze how often you collaborate"""
        years = defaultdict(lambda: {'solo': 0, 'collaborative': 0})
        
        for paper in papers:
            year = paper.get('year', datetime.now().year)
            author_count = len(paper.get('authors', []))
            
            if author_count == 1:
                years[year]['solo'] += 1
            else:
                years[year]['collaborative'] += 1
        
        return dict(years)
    
    def _empty_analysis(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'total_collaborators': 0,
            'total_collaborations': 0,
            'network_metrics': {},
            'strategic_collaborators': [],
            'collaboration_frequency': {}
        }
    
    def _save_analysis(self, analysis: Dict, analysis_type: str):
        filename = f"{analysis_type}_{datetime.now().strftime('%Y%m%d')}.json"
        output_file = self.processed_data / filename
        
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        latest_file = self.processed_data / f"{analysis_type}_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(analysis, f, indent=2)

if __name__ == '__main__':
    data_dir = Path.home() / 'AcademicSync/SRE/observatory/data'
    analyzer = NetworkAnalyzer(data_dir)
    results = analyzer.analyze_network()
    print(json.dumps(results, indent=2))
