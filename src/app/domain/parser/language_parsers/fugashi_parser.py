import re

import jaconv
from fugashi import Tagger, UnidicNode
from konoha import SentenceTokenizer

from app.config.base import get_user_settings
from app.domain.parser.language_parsers.language_parser import LanguageParser
from app.domain.parser.language_parsers.paser_config import register_parser
from app.domain.parser.markdown_text_parser import WordToken

# from .parser_tool import register_parser

# CSJ_PATH = r"C:Users\fanzh\PycharmProjects\lute-backend\data\csj"
# csj_path = pathlib.Path(CSJ_PATH).as_posix()
CWJ_PATH = get_user_settings().unidic_cwj_path_str
POS_TAGS = {
    "代名詞",
    "副詞",
    "助動詞",
    "助詞",
    "動詞",
    "名詞",
    "形容詞",
    "形状詞",
    "感動詞",
    "接尾辞",
    "接続詞",
    "接頭辞",
    "空白",
}


class JapaneseHelper:
    kana_regex = re.compile("[\u3040-\u309F\u30A0-\u30FFー]+")

    @classmethod
    def string_is_kana(cls, text: str) -> bool:
        return bool(cls.kana_regex.fullmatch(text))

    @staticmethod
    def kata2hira(katakana: str) -> str:
        return str(jaconv.kata2hira(katakana))

    # @staticmethod
    # def pos2ud(pos:str):
    #     f = {"接頭辞": "NOUN", "接頭詞": "NOUN", "代名詞": "PRON", "連体詞": "DET", "副詞": "ADV", "感動詞": "INTJ",
    #          "フィラー": "INTJ", "接続詞": "CCONJ", "補助記号": "PUNCT"}
    #
    #


@register_parser("fugashi")
class JapaneseFugashiParser(LanguageParser):
    def __init__(self, language_name: str, **kwargs: str) -> None:
        super().__init__(language_name)
        self._tagger = Tagger(kwargs["undic_path"])
        self._sentence_tokenizer = SentenceTokenizer()

    def tokenize(self, text: str) -> list[WordToken]:
        token: UnidicNode
        res = []
        pos_set = set()
        for token in self._tagger(text):
            pos_extra = (token.feature.pos1, token.feature.pos2, token.feature.pos3, token.feature.pos4)
            # if token.feature.pos1 not in POS_TAGS:
            #     raise ValueError(f"Unknown POS tag: {token.feature.pos1}")
            word_token = WordToken(
                word_string=token.surface,
                word_lemma=token.feature.orthBase,
                word_pos=token.feature.pos1,
                is_word=token.char_type in {2, 6, 7, 8},
                pos_extra=",".join(pos_extra),
            )
            pos_set.add((token.feature.pos1, token.feature.pos2, token.feature.pos3, token.feature.pos4))
            if token.feature.goshu == "外":
                word_token.word_pronunciation = token.feature.lemma.split("-")[-1]
            elif JapaneseHelper.string_is_kana(token.surface) or not token.feature.kana:
                word_token.word_pronunciation = ""
            else:
                word_token.word_pronunciation = JapaneseHelper.kata2hira(token.feature.kana)
            res.append(word_token)
        return res

    def split_sentences(self, text: str) -> list[str]:
        return self._sentence_tokenizer.tokenize(text)  # type: ignore[no-any-return]

    def split_sentences_and_tokenize(self, text: str) -> list[list[WordToken]]:
        return [self.tokenize(sentence) for sentence in self.split_sentences(text)]


if __name__ == "__main__":
    parser = JapaneseFugashiParser("fugashi", undic_path=CWJ_PATH)
    # print(parser.tokenize("李さんは毎朝、六時に起きます。"))
