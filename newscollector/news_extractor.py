import abc
import collections

from bs4 import BeautifulSoup

from newscollector import common
from newscollector.raw_news import BBCRawArticle, FlightLandingUpdate

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
        return html_tag_class_name is None or (
                html_tag_class_name != 'story-body__introduction' and
                'twite' not in html_tag_class_name)

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


class FlightLandingScheduleExtractor(NewsExtractor):
    def extract_raw_news(self):
        soup = BeautifulSoup(self.news_file_content, common.WEB_SCRAPPING_PARSER)
        schedule_update_message = soup.find(id=common.AIRPORT_SCHEDULE_UPDATE_TAG_ID).text
        schedule_update_time = common.extract_airport_schedule_update_time(schedule_update_message)
        all_landing_tags = soup.find_all(name='tr', attrs={'class': ['odd', 'even']})[1:]
        return [self._extract_landing_update(tag, schedule_update_time) for tag in all_landing_tags]

    @classmethod
    def _extract_landing_update(cls, landing_html_row, schedule_update_time):
        flight_company = cls._extract_flight_company(landing_html_row)
        flight_number = landing_html_row.find(name='td', attrs={'class': 'FlightNum'}).text.strip()
        flight_from = landing_html_row.find(name='td', attrs={'class': 'FlightFrom'}).find(
            'span').text.strip()
        planned_time = landing_html_row.find(name='td', attrs={'class': 'FlightTime'}).text.strip()
        updated_time = landing_html_row.find(name='td', attrs={'class': 'finalTime'}).text.strip()
        local_terminal = int(
            landing_html_row.find(name='td', attrs={'class': 'localTerminal'}).text)
        status = landing_html_row.find(name='td', attrs={'class': 'status'}).find(
            'div').text.strip()
        return FlightLandingUpdate(schedule_update_time, flight_company, flight_number, flight_from,
                                   planned_time, updated_time, local_terminal, status)

    @staticmethod
    def _extract_flight_company(flight_html_row):
        flight_company_element_tag = flight_html_row.find(name='td', attrs={'class': 'flightIcons'})
        logo_image_tag = flight_html_row.find(name='img', attrs={'class': 'logoImg'})
        if logo_image_tag:
            return logo_image_tag['alt'].strip()
        return flight_company_element_tag.find(name='span', attrs={'class': 'noIcon'}).text.strip()


if __name__ == '__main__':
    all_schedules = FlightLandingScheduleExtractor(
        '/Users/tamir/PycharmProjects/newscollector/newscollector/output/flights_schedule_2019-10-20 23:06:28.387212.html').extract_raw_news()
    print all_schedules[0].to_dict()
