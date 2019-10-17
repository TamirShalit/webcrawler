import abc
import collections
import json
import os
from datetime import datetime

from bs4 import BeautifulSoup

from newscollector import common
from newscollector.raw_news import BBCRawArticle

FlightData = collections.namedtuple('FlightData',
                                    ['number', 'flight_from', 'planned_time', 'updated_time',
                                     'terminal', 'status'])


class NewsExtractor(object):
    """Extracts relevant raw data from downloaded news files."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, news_file_path, output_directory):
        self.news_file_path = news_file_path
        self._news_file_content = ''
        self.output_directory = output_directory

    @property
    def news_file_content(self):
        if self._news_file_content:
            return self._news_file_content
        with open(self.news_file_path) as news_file:
            return news_file.read()

    def reload_news_file(self):
        self._news_file_content = ''
        return self.news_file_content

    @abc.abstractmethod
    def extract_raw_news(self):
        """
        Extract raw news from news file.
        :rtype: list[newscollector.raw_news.RawNews]
        """


class BBCNewsExtractor(NewsExtractor):
    @staticmethod
    def _is_class_name_of_article_content(html_tag_class_name):
        return html_tag_class_name is None or 'twite' not in html_tag_class_name

    def extract_raw_news(self):
        soup = BeautifulSoup(self.news_file_content, common.WEB_SCRAPPING_PARSER)
        story_body = soup.find(name='div', attrs={'class': 'story-body'})
        article_header = story_body.find(name='h1', attrs={'class': 'story-body__h1'}).text
        article_introduction = story_body.find(name='p',
                                               attrs={'class': 'story-body__introduction'}).text
        article_paragraph_tags = story_body.find_all(
            name=['p', 'h2'],
            attrs={'aria-hidden': '', 'class': self._is_class_name_of_article_content})
        article_paragraphs = [tag.text for tag in article_paragraph_tags]
        return [BBCRawArticle(article_header, article_introduction, article_paragraphs)]


class BenGurionAirportScheduleExtractor(NewsExtractor):

    def extract_raw_news(self):
        soup = BeautifulSoup(self.news_file_content, common.WEB_SCRAPPING_PARSER)
        all_flights_tags = soup.find_all(name='tr', attrs={
            'class': ['odd', 'even']})[1:]
        for tag in all_flights_tags:
            flight_data = self._extract_flight_data(tag)

            flight_data_output_path = os.path.join(self.output_directory,
                                                   '{flight_number} {current_time}.json'.format(
                                                       flight_number=flight_data.number,
                                                       current_time=datetime.now()))
            with open(flight_data_output_path, 'w') as flight_data_output_file:
                json.dump(flight_data._asdict(), flight_data_output_file, indent=2)

    @staticmethod
    def _extract_flight_data(flight_html_row):
        flight_number = flight_html_row.find(name='td', attrs={'class': 'FlightNum'}).text.strip()
        flight_from = flight_html_row.find(name='td', attrs={'class': 'FlightFrom'}).find(
            'span').text.strip()
        planned_time = flight_html_row.find(name='td', attrs={'class': 'FlightTime'}).text.strip()
        updated_time = flight_html_row.find(name='td', attrs={'class': 'finalTime'}).text.strip()
        local_terminal = flight_html_row.find(name='td',
                                              attrs={'class': 'localTerminal'}).text.strip()
        status = flight_html_row.find(name='td', attrs={'class': 'status'}).find('div').text.strip()
        return FlightData(number=flight_number, flight_from=flight_from, planned_time=planned_time,
                          updated_time=updated_time, terminal=local_terminal, status=status)


if __name__ == '__main__':
    raw_news = BBCNewsExtractor(
        "/Users/tamir/PycharmProjects/newscollector/newscollector/Why won't Democrats vote to authorise impeachment_ - BBC News.htm",
        '/Users/tamir/PycharmProjects/newscollector/newscollector/output').extract_raw_news()[0]
    print raw_news.header
    print raw_news.introduction
    print raw_news.paragraphs
    # BenGurionAirportScheduleExtractor(
    #     '/Users/tamir/PycharmProjects/newscollector/newscollector/flights_schedule_2019-10-16 23:48:13.490611.html',
    #     '/Users/tamir/PycharmProjects/newscollector/newscollector/output').extract_raw_news()
