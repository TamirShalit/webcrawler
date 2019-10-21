import abc
import json
from datetime import datetime


class RawNews(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dump(self, file_path):
        """Dump the news to a file."""

    @classmethod
    @abc.abstractmethod
    def load(cls, file_path):
        """Load RawNews from a file."""


class JsonRawNews(RawNews):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_dict(self):
        """
        :rtype: dict
        """

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dictionary):
        pass

    def dump(self, file_path):
        with open(file_path, 'w') as output_file:
            json.dump(self.to_dict(), output_file, indent=2)

    @classmethod
    def load(cls, file_path):
        with open(file_path) as json_file:
            return cls.from_dict(json.load(json_file))


class BBCRawArticle(RawNews):
    END_OF_HEADER = '\n--------END-OF-HEADER----------\n'
    END_OF_INTRODUCTION = '\n--------END-OF-INTRODUCTION----------\n'
    END_OF_PARAGRAPH = '\n--------END-OF-PARAGRAPH----------\n'

    def __init__(self, header, introduction, paragraphs):
        self._header = header
        self._introduction = introduction
        self._paragraphs = paragraphs

    def dump(self, file_path):
        with open(file_path, 'a') as output_file:
            output_file.write(self.header + self.END_OF_HEADER)
            output_file.write(self.introduction + self.END_OF_INTRODUCTION)
            paragraphs = [paragraph.encode('utf-8') + self.END_OF_PARAGRAPH for paragraph in
                          self.paragraphs]
            output_file.writelines(paragraphs)

    @classmethod
    def load(cls, file_path):
        with open(file_path) as raw_article_file:
            content = raw_article_file.read()
        header, after_header = content.split(cls.END_OF_HEADER)
        introduction, after_introduction = after_header.split(cls.END_OF_INTRODUCTION)
        paragraphs = after_introduction.split(cls.END_OF_PARAGRAPH)
        return cls(header, introduction, paragraphs)

    @property
    def header(self):
        return self._header

    @property
    def introduction(self):
        return self._introduction

    @property
    def paragraphs(self):
        return self._paragraphs

    def to_text(self):
        """
        Convert news to a raw text for the use of analyzers.
        :rtype: str
        """
        all_text_chapters = [self.header, self.introduction] + self.paragraphs
        return '\n'.join(all_text_chapters)


class FlightLandingUpdate(JsonRawNews):
    SCHEDULE_UPDATE_TIME_FIELD = 'schedule_update_time'
    COMPANY_FIELD = 'company'
    FLIGHT_NUMBER_FIELD = 'number'
    FLIGHT_FROM_FIELD = 'from'
    PLANNED_TIME_FIELD = 'planned_time'
    UPDATED_TIME_FIELD = 'updated_time'
    TERMINAL_FIELD = 'terminal'
    STATUS_FIELD = 'status'

    SCHEDULE_TIME_FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, schedule_update_time, company, flight_number, flight_from, planned_time,
                 updated_time, terminal, status):
        self._schedule_update_time = schedule_update_time
        self._company = company
        self._flight_number = flight_number
        self._flight_from = flight_from
        self._planned_time = planned_time
        self._updated_time = updated_time
        self._terminal = terminal
        self._status = status

    @property
    def schedule_update_time(self):
        return self._schedule_update_time

    @property
    def company(self):
        return self._company

    @property
    def flight_number(self):
        return self._flight_number

    @property
    def flight_from(self):
        return self._flight_from

    @property
    def planned_time(self):
        return self._planned_time

    @property
    def updated_time(self):
        return self._updated_time

    @property
    def terminal(self):
        return self._terminal

    @property
    def status(self):
        return self._status

    def to_dict(self):
        return {self.SCHEDULE_UPDATE_TIME_FIELD: datetime.strftime(self.schedule_update_time,
                                                                   self.SCHEDULE_TIME_FORMAT),
                self.COMPANY_FIELD: self.company,
                self.FLIGHT_NUMBER_FIELD: self.flight_number,
                self.FLIGHT_FROM_FIELD: self.flight_from,
                self.PLANNED_TIME_FIELD: self.planned_time,
                self.UPDATED_TIME_FIELD: self.updated_time,
                self.STATUS_FIELD: self.status}

    @classmethod
    def from_dict(cls, dictionary):
        return cls(datetime.strptime(dictionary[cls.SCHEDULE_UPDATE_TIME_FIELD],
                                     cls.SCHEDULE_TIME_FORMAT),
                   dictionary[cls.COMPANY_FIELD],
                   dictionary[cls.FLIGHT_NUMBER_FIELD],
                   dictionary[cls.FLIGHT_FROM_FIELD],
                   dictionary[cls.PLANNED_TIME_FIELD],
                   dictionary[cls.UPDATED_TIME_FIELD],
                   dictionary[cls.TERMINAL_FIELD],
                   dictionary[cls.STATUS_FIELD])
