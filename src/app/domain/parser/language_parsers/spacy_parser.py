from functools import lru_cache

import spacy
from spacy.language import Language

from app.domain.parser.markdown_text_parser import WordToken

# from app.lib.timer import sync_timed
from .language_parser import LanguageParser
from .parser_tool import register_parser
from .paser_config import spacy_model_mapping

__all__ = ("SpacyParser", "split_sentences_and_tokenize")


@lru_cache
def split_sentences_and_tokenize(nlp: Language, text: str) -> list[list[WordToken]]:
    res = []
    for sent in nlp(text).sents:
        sentence_tokens = [
            WordToken(
                word_string=token.text,
                word_pos=token.pos_,
                word_lemma=token.lemma_,
                is_word=not token.is_punct,
                next_is_ws=" " in token.text_with_ws,
            )
            for token in sent
        ]
        res.append(sentence_tokens)
    return res


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

    def split_sentences_and_tokenize(self, text: str) -> list[list[WordToken]]:
        return split_sentences_and_tokenize(self.nlp, text)

    def tokenize(self, text: str) -> list[WordToken]:
        return [
            WordToken(
                word_string=token.text,
                word_pos=token.pos_,
                word_lemma=token.lemma_,
                is_word=not token.is_punct,
                next_is_ws=" " in token.text_with_ws,
            )
            for token in self.nlp(text)
        ]
