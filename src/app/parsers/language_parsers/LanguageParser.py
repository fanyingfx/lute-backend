import abc
from abc import ABC

__all__ = ("LanguageParser",)


class Singleton:
    _instances = {}

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instances:
            self._instances[self._cls] = self._cls(*args, **kwargs)
        return self._instances[self._cls]


class LanguageParser(ABC):
    language_name = None

    @classmethod
    @abc.abstractmethod
    def get_language_name(cls):
        """

        Returns:

        """
        raise NotImplementedError

    def load_resource(self, resource):  # noqa
        ...

    def update_resource(self, resource):  # noqa
        ...

    @abc.abstractmethod
    def split_sentences(self, text):
        pass

    @abc.abstractmethod
    def split_sentences_and_tokenize(self, text):
        pass

    @abc.abstractmethod
    def tokenize(self, text):
        pass
