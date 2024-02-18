import abc

__all__ = ("LanguageParser", "Singleton")

from collections.abc import Iterable
from typing import Any, ClassVar

from spacy.tokens.span import Span

from app.domain.words.models import Word


class Singleton:
    _instances: dict[str, list[Word]] = {}

    def __init__(self, cls):  # type: ignore
        self._cls = cls

    def __call__(self, *args, **kwargs):  # type: ignore
        if self._cls not in self._instances:
            self._instances[self._cls] = self._cls(*args, **kwargs)
        return self._instances[self._cls]


class LanguageParser(metaclass=abc.ABCMeta):
    language_name: ClassVar[str | None] = None
    class_instances: dict[type, "LanguageParser"] = {}

    @classmethod
    @abc.abstractmethod
    def get_language_name(cls) -> str:
        """

        Returns:

        """
        raise NotImplementedError

    def load_resource(self, resource: Any) -> Any:  # noqa
        ...

    def update_resource(self, resource: Any) -> Any:  # noqa
        ...

    @classmethod
    @abc.abstractmethod
    def split_sentences(cls, text: str) -> list[Span]:
        pass

    @classmethod
    @abc.abstractmethod
    def split_sentences_and_tokenize(cls, text: str) -> list[Span]:  # TODO replace Span with Sentence
        pass

    @classmethod
    @abc.abstractmethod
    def tokenize(cls, text: str) -> Iterable[Any]:
        pass
