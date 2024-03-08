from collections.abc import Iterator
from functools import lru_cache

import spacy
from spacy.language import Language

from app.domain.parser.markdown_text_parser import WordToken

# from app.lib.timer import sync_timed
from .language_parser import LanguageParser
from .parser_tool import register_parser, spacy_model_mapping

__all__ = ("SpacyParser", "split_sentences_and_tokenize")


@lru_cache
def split_sentences_and_tokenize(nlp: Language, text: str) -> Iterator[Iterator[WordToken]]:
    for sent in nlp(text).sents:
        yield (
            WordToken(
                word_string=token.text,
                word_pos=token.pos_,
                word_lemma=token.lemma_,
                is_word=not token.is_punct,
                next_is_ws=" " in token.text_with_ws,
                is_eos=bool(token.is_sent_end),
            )
            for token in sent
        )


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

    def split_sentences_and_tokenize(self, text: str) -> Iterator[Iterator[WordToken]]:  # type: ignore
        return split_sentences_and_tokenize(self.nlp, text)

    def tokenize(self, text) -> Iterator[WordToken]:  # type: ignore
        for token in self.nlp(text):
            yield WordToken(
                word_string=token.text,
                word_pos=token.pos_,
                word_lemma=token.lemma_,
                is_word=not token.is_punct,
                next_is_ws=" " in token.text_with_ws,
                is_eos=token.is_sent_end,
            )
