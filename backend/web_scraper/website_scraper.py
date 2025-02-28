# backend/web_scraper/website_scraper.py

import requests
from bs4 import BeautifulSoup
import re

class WebsiteScraper:
    def __init__(self, base_url):
        """
        Initialize the scraper with the target base URL.
        :param base_url: The website to scrape.
        """
        self.base_url = base_url

    def fetch_page(self, url):
        """
        Fetch the page content from the URL.
        :param url: URL to fetch
        :return: Parsed HTML content
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Failed to retrieve {url}, Status Code: {response.status_code}")
            return None

    def extract_text(self, url):
        """
        Extract text content from a given page.
        :param url: URL of the page
        :return: Extracted text
        """
        soup = self.fetch_page(url)
        if soup:
            paragraphs = soup.find_all("p")
            text_content = " ".join([para.get_text() for para in paragraphs])
            return text_content
        return ""

    def extract_images(self, url):
        """
        Extract all image URLs from a given page.
        :param url: URL of the page
        :return: List of image URLs
        """
        soup = self.fetch_page(url)
        if soup:
            images = soup.find_all("img", src=True)
            image_urls = [img["src"] if img["src"].startswith("http") else self.base_url + img["src"] for img in images]
            return image_urls
        return []

    def search_for_keywords(self, url, keywords):
        """
        Search for specific keywords on a webpage.
        :param url: URL of the page
        :param keywords: List of keywords to search for
        :return: Dictionary with keyword occurrences
        """
        text_content = self.extract_text(url)
        keyword_matches = {keyword: len(re.findall(keyword, text_content, re.IGNORECASE)) for keyword in keywords}
        return keyword_matches

if __name__ == "__main__":
    scraper = WebsiteScraper("https://example.com")
    target_url = "https://example.com/sample-page"
    
    print("Extracted Text:")
    print(scraper.extract_text(target_url))

    print("\nExtracted Images:")
    print(scraper.extract_images(target_url))

    print("\nKeyword Matches:")
    keywords_to_search = ["copyright", "patent", "trademark"]
    print(scraper.search_for_keywords(target_url, keywords_to_search))
