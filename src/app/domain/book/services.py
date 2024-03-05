from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.db.models.book import Book, BookText
from app.domain.parser.markdown_text_parser import (
    ParsedTextSegment,
    Segment,
    SentenceSegment,
    TextRawParagraphSegment,
    VWord,
)
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService
from app.lib.timer import async_timed  # type: ignore

if TYPE_CHECKING:
    from collections.abc import Iterable

    from spacy.tokens import Token
    from spacy.tokens.span import Span
    from sqlalchemy.orm import InstrumentedAttribute

    from app.domain.book.dtos import BookTextCreate
    from app.domain.parser.language_parser import LanguageParser
    from app.domain.word.services import WordIndex

__all__ = ["BookService", "BookTextService"]


class BookRepository(SQLAlchemyAsyncRepository[Book]):
    """Book SQLAlchemy Repository."""

    model_type = Book


class BookTextRepository(SQLAlchemyAsyncRepository[BookText]):
    """BookText SQLAlchemy Repository."""

    model_type = BookText


class BookService(SQLAlchemyAsyncRepositoryService[Book]):
    """Handles database operations for users."""

    repository_type = BookRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: BookRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create_with_contents(self, data: Book | dict[str, Any], contents: list[BookTextCreate]) -> Book:
        book_obj = await self.to_model(data, "create")
        book = await super().create(data=book_obj, auto_commit=False)
        for content in contents:
            book.texts.append(BookText(ref_book_id=book.id, book_text=content.book_text, title=content.book_title))
        return await self.update(item_id=book.id, data=book)

    async def create(
        self,
        data: Book | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> Book:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def update(
        self,
        data: Book | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> Book:
        return await super().update(item_id=item_id, data=data, auto_commit=True)

    async def update_bookname(self, data: dict[str, Any], db_obj: Book) -> None:
        """Update stored user password.

        This is only used when not used IAP authentication.
        """
        db_obj.book_name = data.get("book_name")  # type: ignore[assignment]
        await self.repository.update(db_obj)

    async def to_model(self, data: Book | dict[str, Any], operation: str | None = None) -> Book:
        return await super().to_model(data, operation)


class BookTextService(SQLAlchemyAsyncRepositoryService[BookText]):
    """Handles database operations for users."""

    repository_type = BookTextRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: BookTextRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(
        self,
        data: BookText | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> BookText:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def update(
        self,
        data: BookText | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> BookText:
        db_obj = await self.to_model(data, "update")
        return await super().update(item_id=item_id, data=db_obj, auto_commit=auto_commit)

    async def to_model(self, data: BookText | dict[str, Any], operation: str | None = None) -> BookText:
        return await super().to_model(data, operation)


async def match_word_in_sentence(sentence: Span, word_index: WordIndex, max_loop_num: int) -> SentenceSegment:
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
            word_pronunciation="",
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


@async_timed  # type: ignore
async def text2segment(text: str, language_parser: LanguageParser, paragraph_order: int) -> list[SentenceSegment]:
    """
    Returns:
        object: TextParagraphSegment
    """
    sents: list[Span] = language_parser.split_sentences_and_tokenize(text)
    max_loop_num = len(text) * 100
    from app.domain.word.services import words_store

    language_name = language_parser.get_language_name()
    word_index: WordIndex = await words_store.get(f"{language_name}-word-index")  # type: ignore
    sentences = []
    for index, sent in enumerate(sents, 1):
        parsed_sent = await match_word_in_sentence(sent, word_index, max_loop_num)
        parsed_sent.paragraph_order = paragraph_order
        parsed_sent.sentence_order = index
        sentences.append(parsed_sent)
    return sentences


async def get_parsed_text_segments(segmentlist: list[Segment], parser: LanguageParser) -> list[ParsedTextSegment]:
    paragraph_order = 1
    res: list[ParsedTextSegment] = []
    for segment in segmentlist:
        if isinstance(segment, TextRawParagraphSegment):
            sentence_segments = await text2segment(segment.segment_value, parser, paragraph_order)
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
