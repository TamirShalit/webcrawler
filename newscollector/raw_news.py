import abc


class RawNews(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dump(self, file_path):
        """Dump the news to a file."""

    @classmethod
    @abc.abstractmethod
    def load(cls, file_path):
        """Load RawNews from a file."""
