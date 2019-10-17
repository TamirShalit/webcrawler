import abc
import os


class RawNews(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dump(self, file_path):
        """Dump the news to a file."""

    @classmethod
    @abc.abstractmethod
    def load(cls, file_path):
        """Load RawNews from a file."""

    @classmethod
    def load_directory(cls, directory_path):
        """Load RawNews from all files in a directory."""
        all_file_paths = []
        for file_name in os.listdir(directory_path):
            all_file_paths.append(os.path.join(directory_path, file_name))
        return [cls.load(file_path) for file_path in all_file_paths]


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
            output_file.writelines(
                [paragraph + self.END_OF_PARAGRAPH for paragraph in self.paragraphs])

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
