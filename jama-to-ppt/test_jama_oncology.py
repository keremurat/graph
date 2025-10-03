#!/usr/bin/env python3
"""
Test script for JAMA Oncology PowerPoint format
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ppt_generator_jama_oncology import JAMAOncologyPowerPointGenerator

# Sample data from reference image
article_data = {
    'title': 'Ribociclib Plus Endocrine Therapy in Hormone Receptor-Positive/ERBB2-Negative Early Breast Cancer',
    'authors': 'Fasching PA, Stroyakovskiy D, Yardley DA, et al',
    'publication_date': 'September 25, 2025',
    'doi': '2025.3700',
    'population': '''20 Males, 5081 Females

Adults with high-risk stage II or III hormone receptor-positive/ERBB2-negative early breast cancer

Median age: 52 (range, 24-90) y''',
    'intervention': '''5101 Patients randomized

2549 Ribociclib plus nonsteroidal aromatase inhibitor (NSAI)
Experimental arm

2552 NSAI alone
Control arm''',
    'setting': '''384 Sites in 20 countries''',
    'primary_outcome': '''The primary end point was invasive disease-free survival (iDFS), which was defined according to Standardized Definitions for Efficacy Endpoints criteria, version 1.0, as assessed by the investigator''',
    'finding_1': '''With a median follow-up beyond the 3-y treatment duration and all patients completing or discontinuing ribociclib, there was consistent iDFS benefit with ribociclib plus NSAI vs NSAI alone

iDFS
Ribociclib + NSAI: 263 events (10.3%)
NSAI alone: 340 events (13.3%)
Hazard ratio: 0.72; 95% CI, 0.61-0.84''',
    'finding_2': 'Additional findings'
}

def main():
    print("=" * 60)
    print("🎯 JAMA Oncology Format Test")
    print("=" * 60)
    print()

    output_path = "output/test_jama_oncology.pptx"

    print("📝 Generating JAMA Oncology PowerPoint...")
    generator = JAMAOncologyPowerPointGenerator(article_data, verbose=True)
    generator.generate(output_path)

    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print(f"📁 File: {output_path}")
    print()

if __name__ == '__main__':
    main()
