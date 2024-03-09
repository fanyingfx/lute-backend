from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from .paser_config import parser_mapping

__all__ = ("register_parser", "list_all_parsers", "parser_exists", "match_word_in_sentence")

from .paser_config import fugashi_unidic, spacy_model_mapping

if TYPE_CHECKING:
    from app.db.models.word import Word
    from app.domain.parser.markdown_text_parser import WordToken

    from .language_parser import LanguageParser
from app.domain.parser.markdown_text_parser import (
    ParsedTextSegment,
    Segment,
    SentenceSegment,
    TextRawParagraphSegment,
    VWord,
)


def register_parser(parser_name: str) -> Callable[[type[LanguageParser]], type[LanguageParser]]:
    def wrapper(cls: type[LanguageParser]) -> type[LanguageParser]:
        if parser_name in parser_mapping:
            raise ValueError(f"Parser {parser_name} is already registered")
        if parser_name == "spacy":
            for key in spacy_model_mapping:
                parser_mapping[key] = cls
        elif parser_name == "fugashi":
            for key in fugashi_unidic:
                parser_mapping[key] = cls
        else:
            parser_mapping[parser_name] = cls
        return cls

    return wrapper


def list_all_parsers() -> list[str]:
    return list(parser_mapping.keys())


def parser_exists(parser_name: str) -> bool:
    return parser_name in parser_mapping


async def match_word_in_sentence(
        sentence_iter: list[WordToken], word_index: dict[str, list[Word]], max_loop_num: int
) -> SentenceSegment:
    start_position = 0
    res_word_list = []
    dead_loop_indicator = 0
    sentence = [*sentence_iter]
    sentence_length = len(sentence)
    sentence_raw = str(sentence)

    while start_position < sentence_length:
        current_word = sentence[start_position].word_string
        current_token: WordToken = sentence[start_position]
        vword: VWord = VWord(**current_token.__dict__, word_tokens=[current_token.word_string])

        if current_word in word_index:
            for db_word in word_index[current_word]:
                end_position = start_position
                for word_token in db_word.word_tokens:
                    if end_position >= sentence_length or word_token != sentence[end_position].word_string:
                        break
                    end_position += 1
                else:
                    # it means all words matches, update word properties with db_word
                    end_position -= 1
                    vword.word_string = db_word.word_string
                    vword.word_lemma = db_word.word_lemma or db_word.word_string
                    vword.word_pos = db_word.word_pos or "UNKNOWN"
                    vword.is_multiple_words = db_word.is_multiple_words
                    vword.is_word = True
                    vword.next_is_ws = sentence[end_position].next_is_ws
                    vword.word_status = db_word.word_status
                    vword.word_explanation = db_word.word_explanation or ""
                    vword.word_pronunciation = db_word.word_pronunciation or ""
                    vword.word_tokens = db_word.word_tokens
                    vword.word_image_src = db_word.word_image.word_image_path if db_word.word_image else None
                    vword.word_db_id = db_word.id
                    start_position = end_position
                    break
        res_word_list.append(vword)

        start_position += 1
        dead_loop_indicator += 1
        if dead_loop_indicator > max_loop_num:
            raise OverflowError(
                f"Maximum number of word in sentence exceeded !{max_loop_num}! or maybe in the dead loop!"
            )
    return SentenceSegment(segment_value=res_word_list, segment_raw=sentence_raw)


async def text2segment(
        text: str, language_parser: LanguageParser, paragraph_order: int, word_index: dict[str, list[Word]]
) -> list[SentenceSegment]:
    """
    Returns:
        object: TextParagraphSegment
    """
    sents: list[list[WordToken]] = language_parser.split_sentences_and_tokenize(text)
    max_loop_num = len(text) * 100

    sentences = []
    for index, sent in enumerate(sents, 1):
        parsed_sent = await match_word_in_sentence(sent, word_index, max_loop_num)
        parsed_sent.paragraph_order = paragraph_order
        parsed_sent.sentence_order = index
        sentences.append(parsed_sent)
    return sentences


async def get_parsed_text_segments(
        segmentlist: list[Segment], parser: LanguageParser, word_index: dict[str, list[Word]]
) -> list[ParsedTextSegment]:
    paragraph_order = 1
    res: list[ParsedTextSegment] = []
    for segment in segmentlist:
        if isinstance(segment, TextRawParagraphSegment):
            sentence_segments = await text2segment(segment.segment_value, parser, paragraph_order, word_index)
            for sentence_segment in sentence_segments:
                res.append(
                    ParsedTextSegment(
                        segment_words=sentence_segment.segment_value,
                        segment_type=sentence_segment.segment_type,
                        paragraph_order=paragraph_order,
                        sentence_order=sentence_segment.sentence_order,
                    )
                )
            paragraph_order += 1
        else:
            res.append(ParsedTextSegment(**segment.__dict__))
    return res
