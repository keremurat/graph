#!/usr/bin/env python3
"""
Debug script to analyze JAMA article structure
"""

import sys
sys.path.insert(0, 'src')

from scraper import JAMAScraper
from bs4 import BeautifulSoup
import re

url = "https://jamanetwork.com/journals/jama/fullarticle/2770277"

print("🔍 Scraping article...")
scraper = JAMAScraper(url, verbose=True)
html_content = scraper.scrape()
soup = scraper.get_soup()

# Save HTML for inspection
with open('debug_article.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("💾 Saved HTML to debug_article.html")

print("\n" + "="*80)
print("📋 ANALYZING ARTICLE STRUCTURE")
print("="*80)

# Check for abstract sections
print("\n1. Looking for Abstract sections...")

# Try different abstract selectors
abstract_selectors = [
    'div.abstract',
    'section.abstract',
    'div[id="abstract"]',
    'div.article-body-section'
]

abstract = None
for selector in abstract_selectors:
    abstract = soup.select_one(selector)
    if abstract:
        print(f"✅ Found abstract: {selector}")
        break

if abstract:
    # Get full text first
    full_text = abstract.get_text(separator='\n', strip=True)
    print(f"\n📝 Abstract text (first 500 chars):\n{full_text[:500]}...\n")

    # Look for structured sections
    sections = abstract.find_all(['p', 'strong', 'h3', 'h4', 'dt', 'dd'])
    for i, section in enumerate(sections[:20]):
        text = section.get_text(strip=True)
        if text and len(text) > 5:
            print(f"  [{i}] {section.name}.{section.get('class', [''])[0]}: {text[:120]}...")

# Check for specific fields
print("\n2. Looking for key sections...")
keywords = ['Importance', 'Objective', 'Design', 'Setting', 'Participants',
            'Intervention', 'Main Outcomes', 'Results', 'Conclusions']

for keyword in keywords:
    # Look for bold/strong tags with keyword
    elements = soup.find_all(['strong', 'b', 'h3', 'h4'],
                            string=re.compile(keyword, re.IGNORECASE))
    if elements:
        for elem in elements[:2]:
            # Get next sibling or parent text
            next_text = ""
            if elem.next_sibling:
                next_text = elem.next_sibling.strip() if isinstance(elem.next_sibling, str) else elem.next_sibling.get_text(strip=True)[:150]
            elif elem.parent:
                next_text = elem.parent.get_text(strip=True)[:150]

            print(f"  ✅ {keyword}: {next_text}...")

print("\n3. Looking for meta tags...")
meta_tags = soup.find_all('meta', attrs={'name': re.compile('citation|dc\\.')})
for meta in meta_tags[:10]:
    print(f"  {meta.get('name')}: {meta.get('content', '')[:80]}")

print("\n" + "="*80)
