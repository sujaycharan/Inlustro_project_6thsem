# backend/web_scraper/google_reverse_search.py

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class GoogleReverseImageSearch:
    def __init__(self, driver_path):
        """
        Initialize the web driver.
        :param driver_path: Path to the Chrome WebDriver
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def search_by_image(self, image_path):
        """
        Perform a reverse image search on Google.
        :param image_path: Path to the image to search
        :return: List of URLs with similar images
        """
        self.driver.get("https://www.google.com/imghp?hl=en")
        time.sleep(2)

        # Click on the camera icon for reverse search
        self.driver.find_element(By.CLASS_NAME, "Gdd5U").click()
        time.sleep(2)

        # Upload the image
        upload_input = self.driver.find_element(By.NAME, "encoded_image")
        upload_input.send_keys(image_path)
        time.sleep(5)  # Wait for results to load

        # Extract search result URLs
        search_results = self.driver.find_elements(By.CSS_SELECTOR, ".rGhul")
        urls = [result.get_attribute("href") for result in search_results]

        self.driver.quit()
        return urls

if __name__ == "__main__":
    searcher = GoogleReverseImageSearch(driver_path="/path/to/chromedriver")
    image_file = "test_image.jpg"
    results = searcher.search_by_image(image_file)
    
    print("Potential Matches Found:")
    for url in results:
        print(url)
