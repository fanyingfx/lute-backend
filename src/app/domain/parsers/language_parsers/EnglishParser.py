from functools import lru_cache

import spacy
from spacy.language import Language
from spacy.tokens.span import Span

# from app.lib.timer import sync_timed
from app.domain.parsers.language_parsers.LanguageParser import LanguageParser

__all__ = ("EnglishParser",)

from app.domain.parsers.language_parsers.LanguageParser import Singleton


@lru_cache
def _split_sentences_and_tokenize(nlp: Language, text: str) -> list[Span]:
    return list(nlp(text).sents)


@Singleton
class EnglishParser(LanguageParser):
    language_name = "english"
    nlp = spacy.load("en_core_web_sm")

    # @lru_cache()
    # def __init__(self)-> NoReturn:  # type: ignore
    #     self.nlp:Language = spacy.load("en_core_web_sm")

    @classmethod
    def split_sentences(cls, text: str):  # type: ignore
        pass

    @classmethod
    def split_sentences_and_tokenize(cls, text: str) -> list[Span]:
        return _split_sentences_and_tokenize(cls.nlp, text)

    @classmethod
    def get_language_name(cls) -> str:
        if not cls.language_name.islower():
            raise ValueError(f"Language name {cls.language_name} is not lowercase")
        return cls.language_name

    @classmethod
    def tokenize(cls, text):  # type: ignore
        pass
