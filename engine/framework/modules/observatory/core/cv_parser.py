#!/usr/bin/env python3
"""
Parse publications from CV and import to database
Based on Mike Edwards' CV (pages 3-5)
"""

from pathlib import Path
from typing import List, Dict, Any
from .database import db

class CVParser:
    """Extract publications from Mike Edwards' CV"""
    
    def __init__(self):
        self.publications = []
    
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse CV and extract peer-reviewed publications
        Based on CV pages 3-5: PEER-REVIEWED PUBLICATIONS section
        """
        
        peer_reviewed = [
            {
                "title": "Insurgent Rhetorics and Historical Materialism",
                "year": 2019,
                "authors": "Mike Edwards",
                "venue": "#Rhetops",
                "publication_type": "book_chapter",
                "doi": None,
                "url": None
            },
            {
                "title": "Open Access and the Economics of Scholarship in Composition Studies",
                "year": 2018,
                "authors": "Mike Edwards, Jessica Reyman",
                "venue": "Rhetoric Review",
                "publication_type": "journal_article",
                "doi": "https://doi.org/10.1080/07350198.2018.1424480",
                "url": None
            },
            {
                "title": "Changing Definitions of Work and Class in the Information Economy",
                "year": 2017,
                "authors": "Mike Edwards, Edie-Marie Roper",
                "venue": "Class in the Composition Classroom: Pedagogy and the Working Class",
                "publication_type": "book_chapter",
                "doi": None,
                "url": None
            },
            {
                "title": "Unpacking the Universal Library: Digital Reading and the Recirculation of Economic Value",
                "year": 2016,
                "authors": "Mike Edwards",
                "venue": "Pedagogy",
                "publication_type": "journal_article",
                "doi": "https://doi.org/10.1215/15314200-3158701",
                "url": None
            },
            {
                "title": "Economies of Writing, Without the Economics: A Rhetorical Analysis of Composition's Economic Discourse in JAC 32.3–4",
                "year": 2014,
                "authors": "Mike Edwards",
                "venue": "Rhetoric Review",
                "publication_type": "journal_article",
                "doi": "https://doi.org/10.1080/07350198.2014.917514",
                "url": None
            },
            {
                "title": "Digital Literacy Instruction in Afghanistan",
                "year": 2014,
                "authors": "Mike Edwards",
                "venue": "Digital Rhetoric and Global Literacies: Communication Modes and Digital Practices in the Networked World",
                "publication_type": "book_chapter",
                "doi": None,
                "url": None
            },
            {
                "title": "Having the Right Stuff Is Only the Beginning: Technology Challenges at West Point",
                "year": 2013,
                "authors": "Mike Edwards, Jeffrey Wilson",
                "venue": "Computers and Composition Online",
                "publication_type": "journal_article",
                "doi": None,
                "url": "http://www2.bgsu.edu/departments/english/cconline/spring2013_special_issue/edwards_wilson/"
            },
            {
                "title": "dot mil: Rhetoric, Technology, and the Military",
                "year": 2010,
                "authors": "Mike Edwards, Alexis Hart",
                "venue": "Kairos: A Journal of Rhetoric, Technology, and Pedagogy",
                "publication_type": "journal_article",
                "doi": None,
                "url": "http://kairos.technorhetoric.net/14.3/index.html"
            },
            {
                "title": "The Teaching and Learning of Web Genres in First-Year Composition",
                "year": 2005,
                "authors": "Mike Edwards, Heidi McKee",
                "venue": "Genre Across the Curriculum",
                "publication_type": "book_chapter",
                "doi": None,
                "url": None
            }
        ]
        
        self.publications = peer_reviewed
        return self.publications
    
    def import_to_database(self):
        """Import parsed publications to database"""
        if not self.publications:
            self.parse()
        
        print(f"\n📚 Importing {len(self.publications)} publications from CV...")
        
        imported = 0
        for pub in self.publications:
            try:
                pub_id = db.add_publication(pub)
                print(f"  ✓ [{pub['year']}] {pub['title'][:65]}...")
                imported += 1
            except Exception as e:
                print(f"  ✗ Error importing: {pub['title'][:50]}... - {e}")
        
        print(f"\n✓ Successfully imported {imported}/{len(self.publications)} publications")
        return imported

def import_cv_publications():
    """Helper function to import publications from CV"""
    parser = CVParser()
    parser.parse()
    return parser.import_to_database()

if __name__ == "__main__":
    import_cv_publications()
    
    # Show what's in the database
    print("\n" + "="*70)
    print("DATABASE CONTENTS AFTER IMPORT")
    print("="*70)
    
    pubs = db.get_publications()
    print(f"\nTotal publications: {len(pubs)}")
    print("\nPublications by year:")
    for pub in pubs:
        authors = pub['authors'].split(',')[0] if ',' in pub['authors'] else pub['authors']
        print(f"  {pub['year']} - {pub['title'][:60]}...")
        print(f"         {authors} et al. in {pub['venue'][:50]}")
        print()
