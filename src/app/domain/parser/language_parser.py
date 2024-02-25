import abc

__all__ = ("LanguageParser", "parser_mapping")

from collections.abc import Iterable
from typing import Any

from spacy.tokens.span import Span

# register in the @parser_tool.register_parser
parser_mapping: dict[str, type["LanguageParser"]] = {}

parser_instances: dict[str, "LanguageParser"] = {}


def _get_parser(language_name: str) -> "LanguageParser":
    if language_name not in parser_instances:
        if language_name not in parser_mapping:
            raise ValueError(f"Parser {language_name} is not registered")
        parser_instances[language_name] = parser_mapping[language_name](language_name)
    return parser_instances[language_name]


class LanguageParser(metaclass=abc.ABCMeta):
    class_instances: dict[type, "LanguageParser"] = {}

    def __init__(self, language_name: str) -> None:
        self.language_name = language_name

    @staticmethod
    def get_parser(parser_name: str) -> "LanguageParser":
        return _get_parser(parser_name)

    def get_language_name(self) -> str:
        return self.language_name

    def load_resource(self, resource: Any) -> Any:  # noqa
        ...

    def update_resource(self, resource: Any) -> Any:  # noqa
        ...

    @abc.abstractmethod
    def split_sentences(self, text: str) -> list[Span]:
        pass

    @abc.abstractmethod
    def split_sentences_and_tokenize(self, text: str) -> list[Span]:  # TODO replace Span with Sentence
        pass

    @abc.abstractmethod
    def tokenize(self, text: str) -> Iterable[Any]:
        pass
