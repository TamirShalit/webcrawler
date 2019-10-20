import abc
import collections

from bs4 import BeautifulSoup

from newscollector import common
from newscollector.raw_news import BBCRawArticle, BenGurionFlightSchedule

FlightData = collections.namedtuple('FlightData',
                                    ['number', 'flight_from', 'planned_time', 'updated_time',
                                     'terminal', 'status'])


class NewsExtractor(object):
    """Extracts relevant raw data from downloaded news files."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, news_file_path):
        self.news_file_path = news_file_path
        self._news_file_content = ''

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
        all_flights_tags = soup.find_all(name='tr', attrs={'class': ['odd', 'even']})[1:]
        return [self._extract_flight_schedule(tag) for tag in all_flights_tags]

    @staticmethod
    def _extract_flight_schedule(flight_html_row):
        flight_number = flight_html_row.find(name='td', attrs={'class': 'FlightNum'}).text.strip()
        flight_from = flight_html_row.find(name='td', attrs={'class': 'FlightFrom'}).find(
            'span').text.strip()
        planned_time = flight_html_row.find(name='td', attrs={'class': 'FlightTime'}).text.strip()
        updated_time = flight_html_row.find(name='td', attrs={'class': 'finalTime'}).text.strip()
        local_terminal = int(flight_html_row.find(name='td', attrs={'class': 'localTerminal'}).text)
        status = flight_html_row.find(name='td', attrs={'class': 'status'}).find('div').text.strip()
        return BenGurionFlightSchedule(flight_number, flight_from, planned_time, updated_time,
                                       local_terminal, status)


if __name__ == '__main__':
    all_schedules = BenGurionAirportScheduleExtractor(
        '/Users/tamir/PycharmProjects/newscollector/newscollector/flights_schedule_2019-10-16 23:48:13.490611.html').extract_raw_news()
    print all_schedules[0].to_dict()
