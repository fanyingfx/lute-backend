import pathlib
import re

import jaconv
from fugashi import Tagger, UnidicNode
from konoha import SentenceTokenizer

from app.domain.parser.markdown_text_parser import WordToken

from .language_parser import LanguageParser
from .parser_tool import register_parser

CSJ_PATH = r"C:Users\fanzh\PycharmProjects\lute-backend\data\csj"
csj_path = pathlib.Path(CSJ_PATH).as_posix()


class JapaneseHelper:
    kana_regex = re.compile("[\u3040-\u309F\u30A0-\u30FFー]+")

    @classmethod
    def string_is_kana(cls, text: str) -> bool:
        return bool(cls.kana_regex.fullmatch(text))

    @staticmethod
    def kata2hira(katakana: str) -> str:
        return str(jaconv.kata2hira(katakana))


@register_parser("fugashi")
class SpokenJapaneseParser(LanguageParser):
    def __init__(self, language_name: str, **kwargs: str) -> None:
        super().__init__(language_name)
        self._tagger = Tagger(kwargs["undic_path"])
        self._sentence_tokenizer = SentenceTokenizer()

    def tokenize(self, text: str) -> list[WordToken]:
        token: UnidicNode
        res = []
        for token in self._tagger(text):
            word_token = WordToken(
                word_string=token.surface,
                word_lemma=token.feature.orthBase,
                word_pos=token.feature.pos1,
                is_word=token.char_type in {2, 6, 7, 8},
            )
            if token.feature.goshu == "外":
                word_token.word_pronunciation = token.feature.lemma.split("-")[-1]
            elif JapaneseHelper.string_is_kana(token.surface):
                word_token.word_pronunciation = ""
            else:
                word_token.word_pronunciation = JapaneseHelper.kata2hira(token.feature.kana)
            res.append(word_token)
        return res

    def split_sentences(self, text: str) -> list[str]:
        return self._sentence_tokenizer.tokenize(text)  # type: ignore[no-any-return]

    def split_sentences_and_tokenize(self, text: str) -> list[list[WordToken]]:
        return [self.tokenize(sentence) for sentence in self.split_sentences(text)]
