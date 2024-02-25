import spacy
from spacy.tokens.span import Span

from app.domain.parser.language_parser import LanguageParser
from app.domain.parser.register_parser import register_parser
from app.domain.parser.spacy_parser import split_sentences_and_tokenize

__all__ = ["JapaneseParser"]


@register_parser("japanese")
class JapaneseParser(LanguageParser):
    def __init__(self, language_name: str) -> None:
        super().__init__(language_name)
        self.nlp = spacy.load("ja_core_news_sm")

    @classmethod
    def split_sentences(cls, text: str):  # type: ignore
        pass

    def split_sentences_and_tokenize(self, text: str) -> list[Span]:  # type: ignore
        return split_sentences_and_tokenize(self.nlp, text)

    def get_language_name(self) -> str:
        return self.language_name

    def tokenize(self, text):  # type: ignore
        return self.nlp(text)
