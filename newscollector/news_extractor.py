import abc
import collections
import json
import os
from datetime import datetime

from bs4 import BeautifulSoup

from newscollector import common

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
        """Extract raw data from news file and write to respective output file/directory."""
        pass


# class BBCNewsExtractor(NewsExtractor):
#     def extract_raw_news(self, news_file):


class BenGurionAirportScheduleExtractor(NewsExtractor):
    def __init__(self, news_file_path, output_directory):
        super(BenGurionAirportScheduleExtractor, self).__init__(news_file_path)
        self.output_directory = output_directory

    def extract_raw_news(self):
        soup = BeautifulSoup(self.news_file_content, common.WEB_SCRAPPING_PARSER)
        all_flights_tags = soup.find_all(name='tr', attrs={
            'class': lambda class_name: class_name in ('odd', 'even')})[1:]
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
    BenGurionAirportScheduleExtractor(
        '/Users/tamir/PycharmProjects/newscollector/newscollector/flights_schedule_2019-10-16 23:48:13.490611.html',
        '/Users/tamir/PycharmProjects/newscollector/newscollector/output').extract_raw_news()
