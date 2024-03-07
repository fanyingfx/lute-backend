from functools import lru_cache

import spacy
from spacy.language import Language
from spacy.tokens.span import Span

# from app.lib.timer import sync_timed
from app.domain.parser.language_parser import LanguageParser
from app.domain.parser.parser_tool import register_parser, spacy_model_mapping

__all__ = ("SpacyParser", "split_sentences_and_tokenize")


@lru_cache
def split_sentences_and_tokenize(nlp: Language, text: str) -> list[Span]:
    return list(nlp(text).sents)


nlp_mapping: dict[str, Language] = {}


def _get_language_parser(language_name: str) -> Language:
    if language_name not in spacy_model_mapping:
        raise NotImplementedError(f"Language {language_name} is not supported")
    if language_name not in nlp_mapping:
        if spacy.util.is_package(spacy_model_mapping[language_name]):
            nlp_mapping[language_name] = spacy.load(spacy_model_mapping[language_name])
        else:
            raise ValueError(
                f"Spacy model {spacy_model_mapping[language_name]} for Language {language_name} is not exists"
            )
    return nlp_mapping[language_name]


@register_parser("spacy")
class SpacyParser(LanguageParser):
    def __init__(self, language_name: str) -> None:
        super().__init__(language_name)
        self.nlp = _get_language_parser(language_name)

    def split_sentences(self, text: str):  # type: ignore
        pass

    def split_sentences_and_tokenize(self, text: str) -> list[Span]:  # type: ignore
        return split_sentences_and_tokenize(self.nlp, text)

    def tokenize(self, text):  # type: ignore
        return self.nlp(text)
