#!/usr/bin/env python3
"""
Check extracted data word counts
"""
import sys
sys.path.insert(0, 'src')

from scraper import JAMAScraper
from extractor import ContentExtractor

url = "https://jamanetwork.com/journals/jama/fullarticle/2770277"

print("🔍 Scraping and extracting...")
scraper = JAMAScraper(url, verbose=False)
html_content = scraper.scrape()
soup = scraper.get_soup()

extractor = ContentExtractor(soup, verbose=False)
data = extractor.extract_all()

print("\n" + "="*70)
print("📊 WORD COUNT CHECK")
print("="*70)

limits = {
    'population': 15,
    'intervention': 15,
    'setting': 10,
    'primary_outcome': 20,
    'finding_1': 15,
    'finding_2': 15
}

for field, limit in limits.items():
    text = data.get(field, '')
    word_count = len(text.split())
    status = "✅" if word_count <= limit else "❌ OVER!"

    print(f"\n{field.upper().replace('_', ' ')}: {status}")
    print(f"  Limit: {limit} words | Actual: {word_count} words")
    print(f"  Text: {text}")

print("\n" + "="*70)
