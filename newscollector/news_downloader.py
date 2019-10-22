import abc
import datetime
import os
import time
import urllib
import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from newscollector import common


class NewsDownloader(object):
    """Downloads data from news website to a directory."""
    __metaclass__ = abc.ABCMeta

    DOWNLOAD_URL = ''

    def __init__(self, download_directory):
        self.download_directory = download_directory

    @abc.abstractmethod
    def download_news(self):
        """Download news from the website to the download directory."""


class SeleniumNewsDownloader(NewsDownloader):
    """Downloads the news using Selenium to bypass security issues."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, download_directory, web_driver_location, driver_type=webdriver.Chrome):
        """
        :param web_driver_location: Location of the web-driver file.
        :param driver_type: Class of Selenium web-driver to use.
        """
        super(SeleniumNewsDownloader, self).__init__(download_directory)
        self._driver_type = driver_type
        self._web_driver_location = web_driver_location
        self._web_driver = None

    def ensure_page_is_open(self):
        if not self.is_driver_open:
            if self._web_driver is not None:
                # Clean everything left from last driver session.
                self._web_driver.quit()
            self._web_driver = self._driver_type(self._web_driver_location)
            self._web_driver.get(self.DOWNLOAD_URL)

    def ensure_page_is_closed(self):
        if self.is_driver_open:
            self._web_driver.close()

    @property
    def is_driver_open(self):
        if self._web_driver is None:
            return False
        try:
            # noinspection PyStatementEffect
            self._web_driver.current_url
            return True
        except WebDriverException:
            return False


class BBCNewsDownloader(NewsDownloader):
    """Downloads articles from BBC main web page and saves them as HTML files."""
    DOWNLOAD_URL = 'http://bbc.com'

    def download_news(self):
        page_source = requests.get(self.DOWNLOAD_URL).text
        soup = BeautifulSoup(page_source, common.WEB_SCRAPPING_PARSER)
        all_article_tags = soup.find_all(name='a', attrs={'class': 'block-link__overlay-link',
                                                          'href': self._is_news_article_url,
                                                          'rev': self._is_rev_of_article})
        for tag in all_article_tags:
            parent_tag_classes = tag.parent['class']
            if parent_tag_classes is None or 'media--icon' not in ''.join(parent_tag_classes):
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

    def _is_news_article_url(self, article_url):
        return article_url.startswith('/news') or 'bbc.com/news' in article_url

    def _is_rev_of_article(self, rev_html_attribute):
        return rev_html_attribute is None or 'video' not in rev_html_attribute

    def _should_download_url(self, article_url):
        is_news_url = article_url.startswith('/news') or 'bbc.com/news' in article_url
        return is_news_url

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


class FlightLandingScheduleDownloader(SeleniumNewsDownloader):
    """
    Downloads real-time schedule of flight landings from Ben-Gurion airport.
    """
    DOWNLOAD_URL = 'http://www.iaa.gov.il/he-IL/airports/BenGurion/Pages/OnlineFlights.aspx'
    SECONDS_BETWEEN_SCHEDULE_UPDATES = 60 * 5
    SECONDS_TO_WAIT_FOR_SCHEDULE_LOADING = 10
    NUMBER_OF_SCHEDULE_PAGES_TO_DOWNLOAD = 3

    _NEXT_PAGE_BUTTON_ID = 'ctl00_rptPaging_ctl06_aNext'
    _SECONDS_TO_WAIT_BETWEEN_PAGE_TOGGLE = 1

    def __init__(self, download_directory, web_driver_location, driver_type=webdriver.Chrome):
        super(FlightLandingScheduleDownloader, self).__init__(download_directory,
                                                              web_driver_location, driver_type)
        self._time_of_last_update_downloaded = None

    def download_news(self):
        update_time = self._wait_for_schedule_update_time()
        self._time_of_last_update_downloaded = update_time
        self._write_schedule_file(self._web_driver.page_source, 1)
        for page_number in xrange(2, self.NUMBER_OF_SCHEDULE_PAGES_TO_DOWNLOAD + 1):
            self._web_driver.find_element_by_id(self._NEXT_PAGE_BUTTON_ID).click()
            time.sleep(self._SECONDS_TO_WAIT_BETWEEN_PAGE_TOGGLE)
            self._write_schedule_file(self._web_driver.page_source, page_number)
        self.ensure_page_is_closed()

    @property
    def time_of_last_update_downloaded(self):
        return self._time_of_last_update_downloaded

    def _click_on_next_page(self):
        try:
            next_button = WebDriverWait(self._web_driver,
                                        self.SECONDS_TO_WAIT_FOR_SCHEDULE_LOADING).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, self._NEXT_PAGE_BUTTON_ID)))
        except TimeoutException:
            self._web_driver.close()
            raise
        next_button.click()

    def download_news_perpetually(self):
        if self.time_of_last_update_downloaded is None:
            self.download_news()
            time.sleep(self.expected_seconds_to_next_update)
        current_schedule_update_time = self._wait_for_schedule_update_time()
        while True:
            while current_schedule_update_time < self.time_of_last_update_downloaded:
                current_schedule_update_time = self._wait_for_schedule_update_time()
            self.download_news()
            time.sleep(self.expected_seconds_to_next_update)
            current_schedule_update_time = self._wait_for_schedule_update_time()

    @property
    def expected_seconds_to_next_update(self):
        time_passed_since_last_update = datetime.datetime.now() - \
                                        self.time_of_last_update_downloaded
        time_left_for_next_update = (datetime.timedelta(
            seconds=self.SECONDS_BETWEEN_SCHEDULE_UPDATES) - time_passed_since_last_update)
        seconds_to_next_update = time_left_for_next_update.total_seconds()
        return seconds_to_next_update if seconds_to_next_update > 0 else 0

    def _wait_for_schedule_update_time(self):
        self.ensure_page_is_open()
        try:
            last_update_message = WebDriverWait(self._web_driver,
                                                self.SECONDS_TO_WAIT_FOR_SCHEDULE_LOADING).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, common.AIRPORT_SCHEDULE_UPDATE_TAG_ID))).text
        except TimeoutException:
            self._web_driver.close()
            raise
        return common.extract_airport_schedule_update_time(last_update_message)

    def _write_schedule_file(self, page_source, page_number):
        download_file_name = 'flights_schedule_page{page_number}_{update_time}.html'.format(
            page_number=page_number, update_time=self.time_of_last_update_downloaded)
        download_file_path = os.path.join(self.download_directory, download_file_name)
        with open(download_file_path, 'w') as download_file:
            download_file.write(page_source.encode('utf-8'))
