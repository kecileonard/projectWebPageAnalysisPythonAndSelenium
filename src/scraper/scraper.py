from src.common import constants
from bs4 import BeautifulSoup
import requests


class Scraper(object):
    def __init__(self, url, page_url=None, search_parameter=None):
        self.url = url
        self.headers = constants.headers
        self.search_parameter = search_parameter
        self.page_url = page_url

    def base_url(self):
        return self.url

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def find_next_page(self):
        if self.search_parameter is not None:
            if self.page_url == 1:
                url_template = f'https://www.scrapingcourse.com/ecommerce/?orderby={self.search_parameter}'
                url = url_template.format(self.search_parameter)
                self.set_url(url)
            else:
                base_template = f'https://www.scrapingcourse.com/ecommerce/page/{self.page_url}/?orderby={self.search_parameter}'
                steam = base_template.format(self.search_parameter)
                url = steam.format(self.page_url)
                self.set_url(url)
            return url
        else:
            if self.page_url == 1:
                url_template = f'https://www.scrapingcourse.com/ecommerce/?orderby={self.search_parameter}'
                url = url_template.format(self.search_parameter)
                self.set_url(url)
            else:
                base_template = f'https://www.scrapingcourse.com/ecommerce/page/{self.page_url}'
                steam = base_template.format(self.search_parameter)
                url = steam.format(self.page_url)
                self.set_url(url)
        return url

    def process_url_request(self):
        response = requests.get(self.find_next_page(), headers=self.headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_page(self):
        """
           This method requests the webpage from the server and
           returns a beautifulsoup element
        """
        try:
            html = self.process_url_request()
            if not html:
                print("error")
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        except Exception as e:
            print(f'problem with webpage\n{e}')
        pass


