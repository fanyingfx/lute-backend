import spacy

from app.domain.parser.markdown_text_parser import WordToken

from .language_parser import LanguageParser
from .parser_tool import register_parser
from .spacy_parser import split_sentences_and_tokenize


@register_parser("japanese")
class JapaneseParser(LanguageParser):
    def __init__(self, language_name: str) -> None:
        super().__init__(language_name)
        try:
            self.nlp = spacy.load("ja_core_news_sm")
        except OSError:
            raise ValueError("ja_core_news_sm is not installed") from None

    @classmethod
    def split_sentences(cls, text: str) -> list[str]:  # type: ignore
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
