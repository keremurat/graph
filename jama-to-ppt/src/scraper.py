"""
JAMA Network Web Scraper with Multi-Tier Fallback System
Enhanced with Playwright and Undetected ChromeDriver for bot detection bypass
"""

import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
try:
    import undetected_chromedriver as uc
    HAS_UC = True
except:
    HAS_UC = False

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except:
    HAS_PLAYWRIGHT = False


class JAMAScraper:
    """
    3-tier fallback web scraping system for JAMA Network articles
    """

    def __init__(self, url: str, verbose: bool = False):
        self.url = url
        self.verbose = verbose
        self.html_content = None
        self.successful_method = None

    def scrape(self) -> str:
        """
        Attempt to scrape using multi-tier fallback system
        Returns HTML content or raises exception
        """
        methods = []

        # Add Playwright if available (best for bot bypass)
        if HAS_PLAYWRIGHT:
            methods.append(("Playwright (stealth)", self._scrape_with_playwright))

        # Add other methods
        if HAS_UC:
            methods.append(("Undetected Chrome", self._scrape_with_undetected_chrome))

        methods.extend([
            ("requests + BeautifulSoup", self._scrape_with_requests),
            ("Selenium (headless)", self._scrape_with_selenium_headless),
            ("Selenium (full browser)", self._scrape_with_selenium_full)
        ])

        for method_name, method_func in methods:
            try:
                if self.verbose:
                    print(f"🔄 Yöntem deneniyor: {method_name}...")

                self.html_content = method_func()

                if self.html_content and len(self.html_content) > 500:
                    self.successful_method = method_name
                    print(f"✅ Başarılı! ({method_name})")
                    return self.html_content
                else:
                    if self.verbose:
                        print(f"⚠️ {method_name} yetersiz içerik döndürdü")

            except Exception as e:
                if self.verbose:
                    print(f"❌ {method_name} başarısız: {str(e)}")
                continue

        raise Exception("❌ Tüm yöntemler denendi, makale çekilemedi. URL'yi kontrol edin veya erişim sorunu olabilir.")

    def _scrape_with_playwright(self) -> str:
        """Method 1: Playwright - best for bot detection bypass"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ])

            context = browser.new_context(
                viewport={'width': random.choice([1920, 1366, 1536]), 'height': random.choice([1080, 768, 864])},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            page = context.new_page()

            try:
                # Navigate and wait for page load
                page.goto(self.url, wait_until='domcontentloaded', timeout=40000)

                # Wait for body to ensure page is loaded
                page.wait_for_selector('body', timeout=10000)

                # Additional wait for dynamic content
                time.sleep(random.uniform(2, 4))

                html_content = page.content()

                # Check if we got meaningful content
                if len(html_content) > 1000:
                    return html_content
                else:
                    raise Exception("Insufficient content received")

            finally:
                browser.close()

    def _scrape_with_undetected_chrome(self) -> str:
        """Method 1: Undetected ChromeDriver - bypasses most bot detection"""
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')  # Use new headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--remote-debugging-port=9222')

        # Random window size to appear more human
        window_sizes = ['1920,1080', '1366,768', '1536,864', '1440,900']
        options.add_argument(f'--window-size={random.choice(window_sizes)}')

        try:
            driver = uc.Chrome(options=options, use_subprocess=True, version_main=140)
        except Exception:
            # Fallback to auto-detect version
            driver = uc.Chrome(options=options, use_subprocess=True)

        try:
            driver.get(self.url)

            # Human-like behavior: random wait
            time.sleep(random.uniform(2, 4))

            # Wait for article content
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )

            # Additional random wait to simulate reading
            time.sleep(random.uniform(1, 2))

            html_content = driver.page_source
            return html_content
        finally:
            try:
                driver.quit()
            except:
                pass

    def _scrape_with_requests(self) -> str:
        """Method 2: Simple requests + BeautifulSoup"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        response = requests.get(self.url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.text

    def _scrape_with_selenium_headless(self) -> str:
        """Method 3: Selenium in headless mode with WSL fixes"""
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9223')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # WSL specific settings
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-tools')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.set_page_load_timeout(30)
            driver.get(self.url)
            # Wait for article content to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            time.sleep(3)  # Additional wait for dynamic content

            html_content = driver.page_source
            return html_content
        finally:
            try:
                driver.quit()
            except:
                pass

    def _scrape_with_selenium_full(self) -> str:
        """Method 4: Selenium with full browser (fallback)"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(self.url)
            # Wait for article content
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            time.sleep(3)  # Extra wait for all dynamic elements

            html_content = driver.page_source
            return html_content
        finally:
            driver.quit()

    def get_soup(self) -> BeautifulSoup:
        """Return BeautifulSoup object from scraped HTML"""
        if not self.html_content:
            self.scrape()

        return BeautifulSoup(self.html_content, 'lxml')
