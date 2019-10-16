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

    WEB_SCRAPPING_PARSER = 'html.parser'
    DOWNLOAD_URL = ''

    def __init__(self, download_directory):
        self.download_directory = download_directory

    @abc.abstractmethod
    def download_news(self):
        """Download news from the website to the download directory."""
        pass


class BBCNewsDownloader(NewsDownloader):
    """Downloads articles from BBC main web page and saves them as HTML files."""
    DOWNLOAD_URL = 'http://bbc.com'

    def download_news(self):
        response = requests.get(self.DOWNLOAD_URL)
        soup = BeautifulSoup(response.text, self.WEB_SCRAPPING_PARSER)
        all_article_tags = soup.find_all(name='a', attrs={'class': 'block-link__overlay-link'})
        for tag in all_article_tags:
            self._download_article_from_html_tag(tag)

    def _download_article_from_html_tag(self, article_tag):
        """
        :param bs4.Tag article_tag: BeatifulSoup tag with link to the article.
        """
        article_url = article_tag['href']
        if article_url.endswith('/'):
            article_url = article_url[:-1]

        urllib.urlretrieve(self._get_article_full_url(article_url),
                           self._get_article_download_destination(article_url))

    def _get_article_download_destination(self, tag_url):
        article_id = tag_url[tag_url.rfind('/') + 1:]
        return os.path.join(self.download_directory, article_id + '.html')

    def _get_article_full_url(self, tag_url):
        is_absolute_url = tag_url.startswith('http')
        if is_absolute_url:
            article_full_url = tag_url
        else:
            article_full_url = urlparse.urljoin(self.DOWNLOAD_URL, tag_url)
        return article_full_url


class BenGurionAirportScheduleDownloader(NewsDownloader):
    """
    Downloads real-time schedule of flights from Ben-Gurion airport.
    Uses Selenium to bypass security issues.
    """
    DOWNLOAD_URL = 'http://www.iaa.gov.il/he-IL/airports/BenGurion/Pages/OnlineFlights.aspx'

    def __init__(self, download_directory, web_driver_location, driver_type=webdriver.Chrome):
        """
        :param web_driver_location: Location of the web-driver file.
        :param driver_type: Class of Selenium web-driver to use.
        """
        super(BenGurionAirportScheduleDownloader, self).__init__(download_directory)
        self._web_driver = driver_type(web_driver_location)

    def _get_page_source(self):
        self._web_driver.get(self.DOWNLOAD_URL)
        source = self._web_driver.page_source
        return source

    def download_news(self):
        soup = BeautifulSoup(self._get_page_source(), self.WEB_SCRAPPING_PARSER)
        flights_table = soup.find(name='table', id='board1')
        for tr in flights_table.find_all('tr'):
            print tr


if __name__ == '__main__':
    # BBCNewsDownloader('/Users/tamir/temp').download_news()
    BenGurionAirportScheduleDownloader('/Users/tamir/temp',
                                       '/Users/tamir/Downloads/chromedriver').download_news()
