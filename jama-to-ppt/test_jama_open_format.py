#!/usr/bin/env python3
"""
Test script for JAMA Open PowerPoint format
Uses sample data from the reference image
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ppt_generator_jama_open import JAMAOpenPowerPointGenerator

# Sample data based on the reference image
article_data = {
    'title': 'Implementation of Group Physical Therapy for Knee Osteoarthritis',
    'authors': 'Allen KD, Webb S, Coffman CJ, et al',
    'publication_date': '2025',
    'doi': '2535038',
    'population': '''130 Men, 14 Women

Sites agreeing to deliver group physical therapy (PT) to adults with symptomatic knee osteoarthritis

Mean age, 67 y''',
    'intervention': '''19 Sites randomized (144 patients)

10 Sites (68 patients)
Enhanced support
Site-specific implementation facilitation, including calls with a trained specialist to address barriers to implementing group PT

9 Sites (76 patients)
Foundational support
Self-guided toolkit and monthly office hour calls to promote the implementation of group PT''',
    'setting': '''19 VA healthcare sites

from January 31, 2022, to March 18, 2024, in outpatient settings''',
    'primary_outcome': '''Penetration, defined as the mean number of patients enrolled in group PT per month during months 7-12 (when enhanced support sites were eligible to receive more intensive support)''',
    'finding_1': '''There was no substantial difference in penetration between enhanced and foundational support sites

Mean penetration (95% CI)
Enhanced support: ~1.0
Foundational support: ~1.0

Mean difference
-0.1 (95% CI, -1.1 to 1.0) patients/mo; P=.92''',
    'finding_2': 'Additional findings not specified'
}

def main():
    print("=" * 60)
    print("🎯 JAMA Open Format Test")
    print("=" * 60)
    print()

    output_path = "output/test_jama_open_format.pptx"

    print("📝 Generating JAMA Open PowerPoint...")
    generator = JAMAOpenPowerPointGenerator(article_data, verbose=True)
    generator.generate(output_path)

    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print(f"📁 File: {output_path}")
    print()

if __name__ == '__main__':
    main()
