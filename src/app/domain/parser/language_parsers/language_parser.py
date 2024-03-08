import abc

__all__ = ("LanguageParser",)

from typing import Any

from app.domain.parser.language_parsers.paser_config import parser_instances, parser_mapping
from app.domain.parser.markdown_text_parser import WordToken

# register in the @parser_tool.register_parser


def _get_parser(language_name: str) -> "LanguageParser":
    from app.domain.parser.language_parsers.paser_config import fugashi_unidic

    if language_name not in parser_instances:
        if language_name not in parser_mapping:
            raise ValueError(f"Parser '{language_name}' is not registered")
        if language_name in fugashi_unidic:
            parser_instances[language_name] = parser_mapping[language_name](
                language_name, undic_path=fugashi_unidic[language_name]
            )
        else:
            parser_instances[language_name] = parser_mapping[language_name](language_name)
    return parser_instances[language_name]


class LanguageParser(abc.ABC):

    def __init__(self, language_name: str, **kwargs: str) -> None:
        self.language_name = language_name

    @staticmethod
    def get_parser(parser_name: str) -> "LanguageParser":
        return _get_parser(parser_name)

    def get_language_name(self) -> str:
        return self.language_name.capitalize()

    def load_resource(self, resource: Any) -> Any:  # noqa
        ...

    def update_resource(self, resource: Any) -> Any:  # noqa
        ...

    @abc.abstractmethod
    def split_sentences(self, text: str) -> list[str]:
        pass

    @abc.abstractmethod
    def split_sentences_and_tokenize(self, text: str) -> list[list[WordToken]]:  # TODO replace Span with Sentence
        pass

    @abc.abstractmethod
    def tokenize(self, text: str) -> list[WordToken]:
        pass
