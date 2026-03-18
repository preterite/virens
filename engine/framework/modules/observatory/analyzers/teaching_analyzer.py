#!/usr/bin/env python3
"""
Teaching Analyzer - Course load tracking and productivity correlation
Monitors: course counts, English 101 vs grad seminars, research productivity links
Contract: 2 courses/semester, 40% teaching / 40% research / 20% service
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import pandas as pd

class TeachingAnalyzer:
    # Course type classifications
    COURSE_TYPES = {
        'english_101': ['College Composition', 'English 101', 'ENGLISH 101', 'Engl 101'],
        'graduate_seminar': ['Graduate Seminar', 'grad seminar', 'ENGLISH 5', 'ENGLISH 6'],
        'other_undergrad': [],  # Will capture anything not in above categories
    }
    
    # Contract expectations
    CONTRACT_COURSES_PER_SEMESTER = 2
    CONTRACT_TEACHING_PERCENT = 40
    CONTRACT_RESEARCH_PERCENT = 40
    CONTRACT_SERVICE_PERCENT = 20
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_data = data_dir / "raw"
        self.processed_data = data_dir / "processed"
        
        # Ensure directories exist
        for directory in [self.raw_data, self.processed_data]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def analyze_teaching(self) -> Dict:
        """Main teaching analysis - run semesterly or on-demand"""
        courses_file = self.raw_data / "teaching_data.json"
        publications_file = self.raw_data / "papers.json"
        
        if not courses_file.exists():
            return self._empty_analysis()
        
        with open(courses_file) as f:
            courses_data = json.load(f)
        
        # Load publications if available for correlation
        publications = []
        if publications_file.exists():
            with open(publications_file) as f:
                pub_data = json.load(f)
                publications = pub_data if isinstance(pub_data, list) else pub_data.get('papers', [])
        
        # Analyze course distribution
        course_distribution = self._analyze_course_distribution(courses_data)
        
        # Contract compliance check
        compliance = self._check_contract_compliance(courses_data)
        
        # Teaching-research correlation
        correlation = self._analyze_teaching_research_correlation(
            courses_data, 
            publications
        )
        
        # Student outcomes (if data available)
        outcomes = self._analyze_student_outcomes(courses_data)
        
        # Semester load patterns
        load_patterns = self._analyze_load_patterns(courses_data)
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'analysis_period': self._get_analysis_period(courses_data),
            'course_distribution': course_distribution,
            'contract_compliance': compliance,
            'teaching_research_correlation': correlation,
            'student_outcomes': outcomes,
            'load_patterns': load_patterns,
            'recommendations': self._generate_recommendations(
                compliance, 
                correlation, 
                load_patterns
            )
        }
        
        self._save_analysis(analysis, 'teaching_analysis')
        
        return analysis
    
    def _analyze_course_distribution(self, courses_data: Dict) -> Dict:
        """Categorize and count course types"""
        distribution = {
            'english_101_count': 0,
            'graduate_seminar_count': 0,
            'other_undergrad_count': 0,
            'total_courses': 0,
            'by_semester': defaultdict(lambda: {
                'english_101': 0,
                'graduate_seminar': 0,
                'other_undergrad': 0
            })
        }
        
        courses = courses_data.get('courses', [])
        
        for course in courses:
            course_name = course.get('name', '')
            course_code = course.get('course_code', '')
            semester = course.get('semester', 'Unknown')
            
            # Classify course
            course_type = self._classify_course(course_name, course_code, course.get('course_type', ''))
            
            # Update counts
            distribution['total_courses'] += 1
            distribution[f'{course_type}_count'] += 1
            distribution['by_semester'][semester][course_type] += 1
        
        # Convert defaultdict to regular dict for JSON serialization
        distribution['by_semester'] = dict(distribution['by_semester'])
        
        return distribution
    
    def _classify_course(self, course_name: str, course_code: str = '', explicit_type: str = '') -> str:
        """Classify course into one of the tracked types.
        Respects explicit course_type if provided (e.g. from backfill data).
        Falls back to name/code pattern matching.
        """
        # Honour explicit classification from data source
        if explicit_type in ('english_101', 'graduate_seminar', 'other_undergrad'):
            return explicit_type
        combined = f"{course_code} {course_name}".lower()
        for type_key, type_names in self.COURSE_TYPES.items():
            if any(name.lower() in combined for name in type_names):
                return type_key
        return 'other_undergrad'
    
    def _check_contract_compliance(self, courses_data: Dict) -> Dict:
        """Check if teaching load matches contract"""
        courses = courses_data.get('courses', [])
        
        # Group by semester
        semester_loads = defaultdict(int)
        for course in courses:
            semester = course.get('semester', 'Unknown')
            semester_loads[semester] += 1
        
        # Check each semester
        compliance_status = {}
        overload_semesters = []
        underload_semesters = []
        
        for semester, count in semester_loads.items():
            if count > self.CONTRACT_COURSES_PER_SEMESTER:
                compliance_status[semester] = 'overload'
                overload_semesters.append({
                    'semester': semester,
                    'courses': count,
                    'excess': count - self.CONTRACT_COURSES_PER_SEMESTER
                })
            elif count < self.CONTRACT_COURSES_PER_SEMESTER:
                compliance_status[semester] = 'underload'
                underload_semesters.append({
                    'semester': semester,
                    'courses': count,
                    'shortage': self.CONTRACT_COURSES_PER_SEMESTER - count
                })
            else:
                compliance_status[semester] = 'compliant'
        
        return {
            'overall_compliant': len(overload_semesters) == 0,
            'semester_status': compliance_status,
            'overload_semesters': overload_semesters,
            'underload_semesters': underload_semesters,
            'service_equity_alert': len(overload_semesters) > 2  # Flag if overloaded multiple times
        }
    
    def _analyze_teaching_research_correlation(
        self, 
        courses_data: Dict, 
        publications: List[Dict]
    ) -> Dict:
        """
        Analyze correlation between teaching load and research output
        Question: Do semesters with English 101 correlate with fewer publications?
        """
        if not publications:
            return {'data_insufficient': True}
        
        # Organize publications by semester/year
        pub_timeline = defaultdict(int)
        for pub in publications:
            pub_date = pub.get('date', '')
            if pub_date:
                try:
                    year = datetime.fromisoformat(pub_date).year
                    pub_timeline[year] += 1
                except:
                    pass
        
        # Organize courses by semester
        courses = courses_data.get('courses', [])
        semester_analysis = {}
        
        for course in courses:
            semester = course.get('semester', '')
            year = self._extract_year_from_semester(semester)
            course_type = self._classify_course(course.get('name', ''), course.get('course_code', ''), course.get('course_type', ''))
            
            if year not in semester_analysis:
                semester_analysis[year] = {
                    'english_101': False,
                    'grad_seminar': False,
                    'total_courses': 0,
                    'publications': pub_timeline.get(year, 0)
                }
            
            semester_analysis[year]['total_courses'] += 1
            if course_type == 'english_101':
                semester_analysis[year]['english_101'] = True
            elif course_type == 'graduate_seminar':
                semester_analysis[year]['grad_seminar'] = True
        
        # Calculate correlation patterns
        english_101_years = [y for y, data in semester_analysis.items() 
                            if data['english_101']]
        other_years = [y for y, data in semester_analysis.items() 
                      if not data['english_101']]
        
        avg_pubs_with_101 = (
            sum(semester_analysis[y]['publications'] for y in english_101_years) / 
            len(english_101_years) if english_101_years else 0
        )
        avg_pubs_without_101 = (
            sum(semester_analysis[y]['publications'] for y in other_years) / 
            len(other_years) if other_years else 0
        )
        
        return {
            'data_sufficient': True,
            'years_analyzed': list(semester_analysis.keys()),
            'avg_pubs_with_english_101': round(avg_pubs_with_101, 2),
            'avg_pubs_without_english_101': round(avg_pubs_without_101, 2),
            'productivity_impact': 'negative' if avg_pubs_with_101 < avg_pubs_without_101 
                                  else 'neutral' if avg_pubs_with_101 == avg_pubs_without_101 
                                  else 'positive',
            'yearly_breakdown': semester_analysis
        }
    
    def _analyze_student_outcomes(self, courses_data: Dict) -> Dict:
        """Analyze student outcomes if data is available"""
        courses = courses_data.get('courses', [])
        
        outcomes = {
            'total_students': 0,
            'courses_with_data': 0,
            'average_enrollment': 0,
            'by_course_type': {}
        }
        
        course_type_stats = defaultdict(lambda: {'count': 0, 'total_students': 0})
        
        for course in courses:
            enrollment = course.get('enrollment', 0)
            if enrollment > 0:
                outcomes['total_students'] += enrollment
                outcomes['courses_with_data'] += 1
                
                course_type = self._classify_course(course.get('name', ''), course.get('course_code', ''), course.get('course_type', ''))
                course_type_stats[course_type]['count'] += 1
                course_type_stats[course_type]['total_students'] += enrollment
        
        if outcomes['courses_with_data'] > 0:
            outcomes['average_enrollment'] = round(
                outcomes['total_students'] / outcomes['courses_with_data'], 
                1
            )
        
        # Calculate averages by type
        for course_type, stats in course_type_stats.items():
            if stats['count'] > 0:
                outcomes['by_course_type'][course_type] = {
                    'avg_enrollment': round(stats['total_students'] / stats['count'], 1),
                    'total_sections': stats['count']
                }
        
        return outcomes
    
    def _analyze_load_patterns(self, courses_data: Dict) -> Dict:
        """Identify patterns in teaching load over time"""
        courses = courses_data.get('courses', [])
        
        patterns = {
            'consecutive_english_101_semesters': 0,
            'consecutive_grad_seminar_semesters': 0,
            'alternating_pattern': False,
            'timeline': []
        }
        
        # Sort courses by semester
        sorted_courses = sorted(
            courses, 
            key=lambda x: self._semester_sort_key(x.get('semester', ''))
        )
        
        # Build timeline
        current_semester = None
        semester_courses = []
        
        for course in sorted_courses:
            semester = course.get('semester', '')
            if semester != current_semester:
                if semester_courses:
                    patterns['timeline'].append({
                        'semester': current_semester,
                        'courses': semester_courses
                    })
                current_semester = semester
                semester_courses = []
            
            semester_courses.append({
                'name': course.get('name', ''),
                'type': self._classify_course(course.get('name', ''), course.get('course_code', ''), course.get('course_type', ''))
            })
        
        # Add final semester
        if semester_courses:
            patterns['timeline'].append({
                'semester': current_semester,
                'courses': semester_courses
            })
        
        # Detect consecutive patterns
        english_101_streak = 0
        grad_seminar_streak = 0
        max_101_streak = 0
        max_grad_streak = 0
        
        for semester_data in patterns['timeline']:
            has_101 = any(c['type'] == 'english_101' for c in semester_data['courses'])
            has_grad = any(c['type'] == 'graduate_seminar' for c in semester_data['courses'])
            
            if has_101:
                english_101_streak += 1
                max_101_streak = max(max_101_streak, english_101_streak)
            else:
                english_101_streak = 0
            
            if has_grad:
                grad_seminar_streak += 1
                max_grad_streak = max(max_grad_streak, grad_seminar_streak)
            else:
                grad_seminar_streak = 0
        
        patterns['consecutive_english_101_semesters'] = max_101_streak
        patterns['consecutive_grad_seminar_semesters'] = max_grad_streak
        
        return patterns
    
    def _generate_recommendations(
        self, 
        compliance: Dict, 
        correlation: Dict,
        load_patterns: Dict
    ) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Contract compliance recommendations
        if not compliance['overall_compliant']:
            if compliance['service_equity_alert']:
                recommendations.append(
                    "⚠️ Service equity concern: Multiple overload semesters detected. "
                    "Consider negotiating course releases or documenting service inequity."
                )
            
            for overload in compliance['overload_semesters']:
                recommendations.append(
                    f"📊 {overload['semester']}: Teaching {overload['courses']} courses "
                    f"(+{overload['excess']} over contract). Request course release or compensation."
                )
        
        # Research productivity recommendations
        if correlation.get('data_sufficient'):
            if correlation['productivity_impact'] == 'negative':
                recommendations.append(
                    f"📉 Research productivity correlation: Semesters with English 101 "
                    f"show {correlation['avg_pubs_without_english_101'] - correlation['avg_pubs_with_english_101']:.1f} "
                    f"fewer publications on average. Consider strategic course scheduling."
                )
        
        # Load pattern recommendations
        if load_patterns['consecutive_english_101_semesters'] >= 3:
            recommendations.append(
                f"🔄 Teaching pattern: {load_patterns['consecutive_english_101_semesters']} "
                f"consecutive semesters with English 101. Consider requesting rotation to "
                f"graduate seminars for research time balance."
            )
        
        if not recommendations:
            recommendations.append("✅ Teaching load appears balanced and contract-compliant.")
        
        return recommendations
    
    def _extract_year_from_semester(self, semester: str) -> Optional[int]:
        """Extract year from semester string (e.g., 'Fall 2024' -> 2024)"""
        try:
            parts = semester.split()
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    return int(part)
        except:
            pass
        return None
    
    def _semester_sort_key(self, semester: str) -> tuple:
        """Generate sort key for semester ordering"""
        year = self._extract_year_from_semester(semester)
        if year is None:
            return (9999, 0)
        
        season_order = {'spring': 1, 'summer': 2, 'fall': 3}
        season = semester.lower().split()[0] if semester else 'unknown'
        season_rank = season_order.get(season, 0)
        
        return (year, season_rank)
    
    def _get_analysis_period(self, courses_data: Dict) -> str:
        """Determine time period covered by analysis"""
        courses = courses_data.get('courses', [])
        if not courses:
            return "No data"
        
        semesters = [c.get('semester', '') for c in courses if c.get('semester')]
        if not semesters:
            return "Unknown period"
        
        sorted_semesters = sorted(
            semesters,
            key=self._semester_sort_key
        )
        
        return f"{sorted_semesters[0]} to {sorted_semesters[-1]}"
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'timestamp': datetime.now().isoformat(),
            'analysis_period': 'No data',
            'course_distribution': {
                'english_101_count': 0,
                'graduate_seminar_count': 0,
                'other_undergrad_count': 0,
                'total_courses': 0,
                'by_semester': {}
            },
            'contract_compliance': {
                'overall_compliant': True,
                'semester_status': {},
                'overload_semesters': [],
                'underload_semesters': [],
                'service_equity_alert': False
            },
            'teaching_research_correlation': {'data_insufficient': True},
            'student_outcomes': {
                'total_students': 0,
                'courses_with_data': 0,
                'average_enrollment': 0,
                'by_course_type': {}
            },
            'load_patterns': {
                'consecutive_english_101_semesters': 0,
                'consecutive_grad_seminar_semesters': 0,
                'alternating_pattern': False,
                'timeline': []
            },
            'recommendations': [
                "⚠️ No teaching data available. Add course information to begin analysis."
            ]
        }
    
    def _save_analysis(self, analysis: Dict, analysis_type: str):
        """Save analysis results with timestamp"""
        filename = f"{analysis_type}_{datetime.now().strftime('%Y%m%d')}.json"
        output_file = self.processed_data / filename
        
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # Also save as "latest"
        latest_file = self.processed_data / f"{analysis_type}_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(analysis, f, indent=2)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'))
    from core.config import config
    data_dir = config.observatory_data
    analyzer = TeachingAnalyzer(data_dir)
    results = analyzer.analyze_teaching()
    print(json.dumps(results, indent=2))
