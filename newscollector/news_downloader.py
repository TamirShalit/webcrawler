import abc
import os
import urllib
import urlparse
from datetime import datetime

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

    def get_page_source(self):
        return requests.get(self.DOWNLOAD_URL).text


class SeleniumNewsDownloader(NewsDownloader):
    """Downloads the news using Selenium to bypass security issues."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, download_directory, web_driver_location, driver_type=webdriver.Chrome):
        """
        :param web_driver_location: Location of the web-driver file.
        :param driver_type: Class of Selenium web-driver to use.
        """
        super(SeleniumNewsDownloader, self).__init__(download_directory)
        self._web_driver = driver_type(web_driver_location)

    def get_page_source(self):
        self._web_driver.get(self.DOWNLOAD_URL)
        source = self._web_driver.page_source
        return source


class BBCNewsDownloader(NewsDownloader):
    """Downloads articles from BBC main web page and saves them as HTML files."""
    DOWNLOAD_URL = 'http://bbc.com'

    def download_news(self):
        soup = BeautifulSoup(self.get_page_source(), self.WEB_SCRAPPING_PARSER)
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


class BenGurionAirportScheduleDownloader(SeleniumNewsDownloader):
    """
    Downloads real-time schedule of flights from Ben-Gurion airport.
    """
    DOWNLOAD_URL = 'http://www.iaa.gov.il/he-IL/airports/BenGurion/Pages/OnlineFlights.aspx'

    def download_news(self):
        page_source = self.get_page_source()
        self._download_news(page_source)

    @staticmethod
    def _download_news(page_source):
        download_file_name = 'flights_schedule_{current_time}.html'.format(
            current_time=datetime.now())
        with open(download_file_name, 'w') as download_file:
            download_file.write(page_source)


if __name__ == '__main__':
    # BBCNewsDownloader('/Users/tamir/temp').download_news()
    BenGurionAirportScheduleDownloader('/Users/tamir/temp',
                                       '/Users/tamir/Downloads/chromedriver').download_news()
