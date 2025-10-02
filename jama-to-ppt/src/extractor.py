"""
Content Extraction Module with Smart Limits and Regex
Enhanced to parse JAMA's structured citation_abstract meta tag
"""

import re
import html
from datetime import datetime
from typing import Dict, Optional, List
from bs4 import BeautifulSoup


class ContentExtractor:
    """
    Extracts structured content from JAMA articles with word limits and smart summarization
    """

    def __init__(self, soup: BeautifulSoup, verbose: bool = False):
        self.soup = soup
        self.verbose = verbose
        self._structured_abstract = None  # Cache for parsed abstract

    def extract_all(self) -> Dict[str, str]:
        """Extract all required fields from article"""
        if self.verbose:
            print("🔍 İçerik analiz ediliyor...")

        data = {
            'title': self._extract_title(),
            'authors': self._extract_authors(),
            'publication_date': self._extract_date(),
            'doi': self._extract_doi(),
            'population': self._extract_population(),
            'intervention': self._extract_intervention(),
            'setting': self._extract_setting(),
            'primary_outcome': self._extract_primary_outcome(),
            'finding_1': self._extract_finding(1),
            'finding_2': self._extract_finding(2),
        }

        if self.verbose:
            print("✅ İçerik çıkarma tamamlandı")

        return data

    def _extract_title(self) -> str:
        """Extract article title"""
        # Try multiple selectors
        selectors = [
            'h1.meta-article-title',
            'h1[property="name"]',
            'h1.article-header__title',
            'h1.content-title',
            'meta[property="og:title"]',
            'title'
        ]

        for selector in selectors:
            if 'meta' in selector or selector == 'title':
                element = self.soup.find('meta', attrs={'property': 'og:title'}) if 'meta' in selector else self.soup.find('title')
                if element:
                    title = element.get('content') if 'meta' in selector else element.get_text()
                    # Clean title
                    title = re.sub(r'\s*\|\s*JAMA.*$', '', title)
                    title = re.sub(r'\s*-\s*JAMA.*$', '', title)
                    return title.strip()
            else:
                element = self.soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)

        return "Article Title Not Found"

    def _extract_authors(self) -> str:
        """Extract authors (first 3 + et al.)"""
        author_selectors = [
            'meta[name="citation_author"]',
            'a.author-name',
            'span.author-name',
            '.meta-article-author-list .author'
        ]

        authors = []

        # Try meta tags first
        meta_authors = self.soup.find_all('meta', attrs={'name': 'citation_author'})
        if meta_authors:
            authors = [tag.get('content') for tag in meta_authors[:3]]
        else:
            # Try other selectors
            for selector in author_selectors[1:]:
                elements = self.soup.select(selector)
                if elements:
                    authors = [el.get_text(strip=True) for el in elements[:3]]
                    break

        if authors:
            if len(authors) >= 3:
                return f"{', '.join(authors)} et al."
            else:
                return ', '.join(authors)

        return "Authors Not Found"

    def _extract_date(self) -> str:
        """Extract publication date"""
        date_selectors = [
            'meta[name="citation_publication_date"]',
            'meta[name="article:published_time"]',
            'time[datetime]',
            '.meta-article-date'
        ]

        for selector in date_selectors:
            if 'meta' in selector:
                element = self.soup.find('meta', attrs={'name': selector.split('[name="')[1].rstrip('"]')})
                if element:
                    date_str = element.get('content')
                    return self._format_date(date_str)
            else:
                element = self.soup.select_one(selector)
                if element:
                    date_str = element.get('datetime') or element.get_text(strip=True)
                    return self._format_date(date_str)

        return datetime.now().strftime("%B %Y")

    def _format_date(self, date_str: str) -> str:
        """Format date to 'Month Year' format"""
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%B %d, %Y', '%d %B %Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime("%B %Y")
                except ValueError:
                    continue

            # If no format works, try to extract year and month
            match = re.search(r'(\d{4})-(\d{2})', date_str)
            if match:
                year, month = match.groups()
                dt = datetime(int(year), int(month), 1)
                return dt.strftime("%B %Y")

        except Exception:
            pass

        return date_str

    def _extract_doi(self) -> str:
        """Extract DOI number"""
        doi_selectors = [
            'meta[name="citation_doi"]',
            'a[href*="doi.org"]',
            '.doi'
        ]

        for selector in doi_selectors:
            if 'meta' in selector:
                element = self.soup.find('meta', attrs={'name': 'citation_doi'})
                if element:
                    doi = element.get('content')
                    return self._clean_doi(doi)
            else:
                element = self.soup.select_one(selector)
                if element:
                    doi = element.get('href') if element.name == 'a' else element.get_text(strip=True)
                    return self._clean_doi(doi)

        return "DOI Not Found"

    def _clean_doi(self, doi: str) -> str:
        """Clean DOI format"""
        # Remove 'doi:' prefix and URL parts
        doi = re.sub(r'^doi:\s*', '', doi, flags=re.IGNORECASE)
        doi = re.sub(r'https?://doi\.org/', '', doi)
        return doi.strip()

    def _get_structured_abstract(self) -> Dict[str, str]:
        """Parse JAMA's structured abstract from citation_abstract meta tag"""
        if self._structured_abstract is not None:
            return self._structured_abstract

        # Try to get from meta tag first (JAMA specific)
        meta_abstract = self.soup.find('meta', attrs={'name': 'citation_abstract'})
        if meta_abstract:
            abstract_html = html.unescape(meta_abstract.get('content', ''))
            # Parse the HTML content
            abstract_soup = BeautifulSoup(abstract_html, 'html.parser')

            sections = {}
            current_section = None

            for elem in abstract_soup.find_all(['h3', 'p']):
                if elem.name == 'h3':
                    current_section = elem.get_text(strip=True)
                    sections[current_section] = ""
                elif elem.name == 'p' and current_section:
                    sections[current_section] = elem.get_text(separator=' ', strip=True)

            self._structured_abstract = sections
            return sections

        # Fallback to regular abstract parsing
        self._structured_abstract = {}
        return {}

    def _get_abstract_text(self) -> str:
        """Extract full abstract text"""
        # First try structured abstract
        structured = self._get_structured_abstract()
        if structured:
            return ' '.join(structured.values())

        # Fallback to DOM selectors
        abstract_selectors = [
            'div.abstract',
            'section.abstract',
            'div[class*="abstract"]',
            '#abstract',
            'div.article-body-section:first-of-type'
        ]

        for selector in abstract_selectors:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(separator=' ', strip=True)

        return ""

    def _extract_population(self) -> str:
        """Extract population/participants info (MAX 15 words)"""
        # Try structured abstract first
        structured = self._get_structured_abstract()

        # JAMA uses "Participants" or "Design, Setting, and Participants"
        for key in ['Participants', 'Design, Setting, and Participants', 'Population']:
            if key in structured:
                text = structured[key]
                # Extract key info about participants
                # Look for patient count, age, condition
                patterns = [
                    r'(\d+\s+(?:participants?|patients?|individuals?|subjects?)[^.;]+?(?:age|years|COVID|ARDS|with|mean)[^.;]+)',
                    r'(Patients? with [^.;]+)',
                    r'(\d+\s+(?:participants?|patients?)[^.;]+)'
                ]

                for pattern in patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        extracted = match.group(1).strip()
                        # Clean up trailing words
                        extracted = re.sub(r'\s+(?:according to|enrolled from|Final).*$', '', extracted, flags=re.IGNORECASE)
                        return self._limit_words(extracted, 15)

                # Otherwise return first sentence
                first_sentence = text.split('.')[0]
                return self._limit_words(first_sentence, 15)

        # Fallback to regex patterns
        abstract = self._get_abstract_text()
        patterns = [
            r'(?:Participants?|Population|Patients?)[:.\s]+([^.]+?)(?:\.|Intervention|Setting|Methods)',
            r'(\d+\s+(?:participants?|patients?|individuals?|subjects?)(?:[^.]+?)(?:aged?|mean age|median age)[^.]+)',
            r'(n\s*=\s*\d+[^.]+?)(?:\.|;)',
        ]

        for pattern in patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                return self._limit_words(text, 15)

        return "Population data not found"

    def _extract_intervention(self) -> str:
        """Extract intervention info (MAX 15 words)"""
        # Try structured abstract first
        structured = self._get_structured_abstract()

        for key in ['Interventions', 'Intervention', 'Exposures']:
            if key in structured:
                text = structured[key]
                # Return first sentence
                first_sentence = text.split('.')[0]
                return self._limit_words(first_sentence, 15)

        # Fallback to regex
        abstract = self._get_abstract_text()
        patterns = [
            r'Intervention[:.\s]+([^.]+?)(?:\.|Main Outcomes?|Results?|Setting)',
            r'(?:received|underwent|assigned to|randomized to)\s+([^.]+?)(?:\.|;|compared)',
            r'(?:Treatment|Therapy|Drug|Medication)[:.\s]+([^.]+?)(?:\.|;)',
        ]

        for pattern in patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                return self._limit_words(text, 15)

        return "Intervention data not found"

    def _extract_setting(self) -> str:
        """Extract setting info (MAX 10 words)"""
        # Try structured abstract first
        structured = self._get_structured_abstract()

        for key in ['Setting', 'Design, Setting, and Participants']:
            if key in structured:
                text = structured[key]
                # Extract setting info (usually first part or mentions location)
                # Look for location patterns
                match = re.search(r'(?:conducted|performed|carried out|in)\s+(.+?)(?:\.|;|Participants)', text, re.IGNORECASE)
                if match:
                    return self._limit_words(match.group(1), 10)
                # Or get first sentence
                first_sentence = text.split('.')[0]
                return self._limit_words(first_sentence, 10)

        # Fallback to regex
        abstract = self._get_abstract_text()
        patterns = [
            r'Setting[:.\s]+([^.]+?)(?:\.|Participants?|Methods?)',
            r'(?:conducted|performed|carried out)\s+(?:at|in)\s+([^.]+?)(?:\.|;)',
            r'(?:hospital|clinic|center|facility|institution)s?\s+(?:in|at|from)\s+([^.]+?)(?:\.|;)',
        ]

        for pattern in patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                return self._limit_words(text, 10)

        return "Setting data not found"

    def _extract_primary_outcome(self) -> str:
        """Extract primary outcome (MAX 20 words)"""
        # Try structured abstract first
        structured = self._get_structured_abstract()

        for key in ['Main Outcomes and Measures', 'Primary Outcome', 'Primary Endpoint', 'Main Outcome Measures']:
            if key in structured:
                text = structured[key]
                # Get first sentence or primary outcome description
                first_sentence = text.split('.')[0]
                return self._limit_words(first_sentence, 20)

        # Fallback to regex
        abstract = self._get_abstract_text()
        patterns = [
            r'(?:Main Outcomes? and Measures?|Primary Outcome|Primary Endpoint)[:.\s]+([^.]+?)(?:\.|Results?)',
            r'(?:measured|assessed|evaluated)\s+([^.]+?mortality|[^.]+?survival|[^.]+?incidence)',
            r'(?:outcome was|endpoint was)\s+([^.]+?)(?:\.|;)',
        ]

        for pattern in patterns:
            match = re.search(pattern, abstract, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                return self._limit_words(text, 20)

        return "Primary outcome not found"

    def _extract_finding(self, number: int) -> str:
        """Extract key findings (MAX 15 words each)"""
        # Try structured abstract first
        structured = self._get_structured_abstract()

        if 'Results' in structured:
            results_text = structured['Results']

            # Split into sentences
            sentences = re.split(r'\.(?:\s+|\s*$)', results_text)
            sentences = [s.strip() for s in sentences if s.strip()]

            # Look for sentences with numerical data
            findings = []
            for sentence in sentences:
                # Prioritize sentences with percentages, p-values, CI, or numbers
                if re.search(r'\d+\.?\d*%|\bp\s*[<>=]\s*0\.\d+|\bn\s*=\s*\d+|95%\s*CI|OR\s*=|HR\s*=|RR\s*=|\d+\s+days', sentence, re.IGNORECASE):
                    findings.append(sentence.strip())

            # If we have enough findings with numbers, use them
            if len(findings) >= number:
                return self._limit_words(findings[number - 1], 15)

            # Otherwise use first N sentences from results
            if len(sentences) >= number:
                return self._limit_words(sentences[number - 1], 15)

        # Fallback to regex parsing
        abstract = self._get_abstract_text()
        results_match = re.search(r'Results?[:.\s]+(.+?)(?:Conclusions?|Discussion|$)', abstract, re.IGNORECASE | re.DOTALL)

        if results_match:
            results_text = results_match.group(1)
            sentences = re.split(r'[.;]\s+', results_text)

            # Look for sentences with numerical data
            findings = []
            for sentence in sentences:
                if re.search(r'\d+\.?\d*%|\bp\s*[<>=]\s*0\.\d+|\bn\s*=\s*\d+|OR\s*=|HR\s*=|RR\s*=', sentence, re.IGNORECASE):
                    findings.append(sentence.strip())

            if len(findings) >= number:
                return self._limit_words(findings[number - 1], 15)

            if len(sentences) >= number:
                return self._limit_words(sentences[number - 1], 15)

        return f"Finding {number} not found"

    def _limit_words(self, text: str, max_words: int) -> str:
        """Limit text to max words and add ellipsis if needed"""
        words = text.split()
        if len(words) > max_words:
            return ' '.join(words[:max_words]) + '...'
        return text

    def _extract_numbers(self, text: str) -> List[str]:
        """Extract numerical data using regex"""
        patterns = [
            r'n\s*=\s*\d+',
            r'\d+\.?\d*%',
            r'p\s*[<>=]\s*0\.\d+',
            r'mean\s+age\s+\d+\.?\d*',
            r'median\s+age\s+\d+\.?\d*',
            r'OR\s*=\s*\d+\.?\d*',
            r'HR\s*=\s*\d+\.?\d*',
            r'RR\s*=\s*\d+\.?\d*',
        ]

        numbers = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            numbers.extend(matches)

        return numbers
