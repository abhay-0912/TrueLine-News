"""
Web Scraper for fetching and parsing news content
"""

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

logger = logging.getLogger(__name__)

class WebScraper:
    """
    Scrapes and extracts content from web pages
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = 10
    
    def scrape(self, url):
        """
        Scrape content from a URL
        
        Args:
            url (str): URL to scrape
        
        Returns:
            str: Extracted text content, or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text if text else None
        
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
    
    def extract_metadata(self, url):
        """
        Extract metadata from a webpage
        
        Args:
            url (str): URL to analyze
        
        Returns:
            dict: Extracted metadata
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            metadata = {
                'url': url,
                'title': soup.title.string if soup.title else 'Unknown',
                'description': self._get_meta_content(soup, 'description'),
                'author': self._get_meta_content(soup, 'author'),
                'publish_date': self._get_meta_content(soup, 'article:published_time'),
                'domain': urlparse(url).netloc
            }
            
            return metadata
        
        except Exception as e:
            logger.warning(f"Error extracting metadata from {url}: {e}")
            return {'url': url, 'domain': urlparse(url).netloc}
    
    def _get_meta_content(self, soup, meta_name):
        """
        Extract content from meta tags
        """
        try:
            meta = soup.find('meta', attrs={'name': meta_name}) or \
                   soup.find('meta', attrs={'property': meta_name})
            return meta.get('content', '') if meta else ''
        except:
            return ''
    
    def check_availability(self, url):
        """
        Check if a URL is accessible
        
        Args:
            url (str): URL to check
        
        Returns:
            bool: True if accessible, False otherwise
        """
        try:
            response = requests.head(url, headers=self.headers, timeout=self.timeout)
            return response.status_code < 400
        except:
            return False
