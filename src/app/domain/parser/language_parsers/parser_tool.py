from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from .language_parser import LanguageParser, parser_mapping

__all__ = ("register_parser", "list_all_parsers", "parser_exists", "match_word_in_sentence")

if TYPE_CHECKING:
    from spacy.tokens import Span, Token

    from app.db.models.word import Word
from app.domain.parser.markdown_text_parser import (
    ParsedTextSegment,
    Segment,
    SentenceSegment,
    TextRawParagraphSegment,
    VWord,
)

spacy_model_mapping = {
    "english": "en_core_web_sm",
}


def register_parser(parser_name: str) -> Callable[[type[LanguageParser]], type[LanguageParser]]:
    def wrapper(cls: type[LanguageParser]) -> type[LanguageParser]:
        if parser_name in parser_mapping:
            raise ValueError(f"Parser {parser_name} is already registered")
        if parser_name == "spacy":
            for key in spacy_model_mapping:
                parser_mapping[key] = cls
        else:
            parser_mapping[parser_name] = cls
        return cls

    return wrapper


def list_all_parsers() -> list[str]:
    return [name.capitalize() for name in parser_mapping]


def parser_exists(parser_name: str) -> bool:
    return parser_name in parser_mapping


async def match_word_in_sentence(
    sentence: list[Token], word_index: dict[str, list[Word]], max_loop_num: int
) -> SentenceSegment:
    start_position = 0
    res_word_list = []
    dead_loop_indicator = 0
    sentence_length = len(sentence)
    sentence_raw = str(sentence)

    while start_position < sentence_length:
        current_word = str(sentence[start_position])
        current_token: Token = sentence[start_position]
        vword = VWord(
            word_string=current_token.text,
            word_lemma=current_token.lemma_,
            word_pos=current_token.pos_,
            is_multiple_words=False,
            is_word=not current_token.is_punct,
            is_eos=current_token.is_sent_end or False,
            next_is_ws=" " in current_token.text_with_ws,
            word_status=0,
            word_explanation="",
            # word_pronunciation=c,
            word_tokens=[current_token.text],
        )

        if current_word in word_index:
            for db_word in word_index[current_word]:
                end_position = start_position
                for word_token in db_word.word_tokens:
                    if end_position >= sentence_length or word_token != str(sentence[end_position]):
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
                    vword.is_eos = sentence[end_position].is_sent_end or False
                    vword.next_is_ws = " " in sentence[end_position].text_with_ws
                    vword.word_status = db_word.word_status
                    vword.word_explanation = db_word.word_explanation
                    vword.word_pronunciation = db_word.word_pronunciation
                    vword.word_tokens = db_word.word_tokens
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
    sents: list[Span] = language_parser.split_sentences_and_tokenize(text)
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
