import abc
from abc import ABC

__all__ = (
    "LanguageParser",
    "SegmentParser",
)


class SegmentParser:
    pass


class LanguageParser(ABC):
    @abc.abstractmethod
    def parse(self, text):
        ...
