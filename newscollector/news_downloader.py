import abc
import os
import urllib
import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class NewsDownloader(object):
    """Downloads articles or other data from news website."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def download_news(self):
        pass


class BBCNewsDownloader(NewsDownloader):
    """Downloads articles from BBC main web page and saves them as HTML files."""

    def __init__(self, download_directory):
        self.download_directory = download_directory

    def download_news(self):
        download_base_url = 'http://bbc.com'
        response = requests.get(download_base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_a_tags = soup.find_all(name='a', attrs={'class': 'block-link__overlay-link'})
        for tag in all_a_tags:
            article_url = tag['href']
            if article_url.endswith('/'):
                article_url = article_url[:-1]
            is_absolute_url = article_url.startswith('http')
            if is_absolute_url:
                article_full_url = article_url
            else:
                article_full_url = urlparse.urljoin(download_base_url, article_url)
            article_id = article_url[article_url.rfind('/') + 1:]
            article_download_destination = os.path.join(self.download_directory,
                                                        article_id + '.html')
            print article_full_url
            print article_id
            print article_download_destination
            urllib.urlretrieve(article_full_url, article_download_destination)


class BenGurionAirportScheduleDownloader(NewsDownloader):
    def __init__(self, download_directory):
        self.download_directory = download_directory

    def get_page_source(self, page):
        web_driver = webdriver.Chrome('/Users/tamir/Downloads/chromedriver')
        web_driver.get(page)
        source = web_driver.page_source
        return source

    def download_news(self):
        download_base_url = 'http://www.iaa.gov.il/he-IL/airports/BenGurion/Pages/OnlineFlights.aspx'
        soup = BeautifulSoup(self.get_page_source(download_base_url), 'html.parser')
        flights_table = soup.find(name='table', id='board1')
        for tr in flights_table.find_all('tr'):
            print tr


if __name__ == '__main__':
    # BBCNewsDownloader('/Users/tamir/temp').download_news()
    BenGurionAirportScheduleDownloader('/Users/tamir/temp').download_news()
