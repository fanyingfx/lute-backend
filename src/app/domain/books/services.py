from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService
from app.parsers.MdTextParser import TextParagraphSegment, TokenSentence

from .models import Book, BookText

if TYPE_CHECKING:
    from collections.abc import Iterable

    from spacy.tokens import Token
    from sqlalchemy.orm import InstrumentedAttribute

    from app.parsers.language_parsers.LanguageParser import LanguageParser
    from app.parsers.WordMatcher import WordIndex

__all__ = ["BookService"]


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

    async def create_with_content(self, data: Book | dict[str, Any], content: str) -> Book:
        book_obj = await self.to_model(data, "create")
        book = await super().create(data=book_obj, auto_commit=False)
        book.texts.append(BookText(ref_book_id=book.id, book_text=content))
        return await self.update(item_id=book.id, data=book)

    async def create(self, data: Book | dict(str, Any)) -> Book:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=True)

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
        db_obj.book_name = data.get("book_name")
        await self.repository.update(db_obj)

    async def to_model(self, data: Book | dict[str, Any], operation: str | None = None) -> Book:
        return await super().to_model(data, operation)


class BookTextService(SQLAlchemyAsyncRepositoryService[BookText]):
    """Handles database operations for users."""

    repository_type = BookTextRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: BookRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(self, data: BookText | dict(str, Any)) -> BookText:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=True)

    async def to_model(self, data: BookText | dict[str, Any], operation: str | None = None) -> BookText:
        return await super().to_model(data, operation)


def match_word_in_sentence(sentence: Iterable[Token], multiple_word_index: WordIndex, single_word_map) -> TokenSentence:
    start_position = 0
    res_word_list = []
    dead_loop_indicator = 0
    sentence_length = len(sentence)

    while start_position < sentence_length:
        current_word = str(sentence[start_position])
        if current_word in multiple_word_index:
            for word in multiple_word_index[current_word]:
                end_position = start_position
                for word_token in word.word_tokens:
                    if end_position >= sentence_length or word_token != str(sentence[end_position]):
                        break
                    end_position += 1
                else:
                    # it means all words matches
                    # TODO add status and else process should return VWord
                    res_word_list.append(sentence[start_position:end_position])
                    start_position = end_position
        else:
            # TODO add condition to judge whether the single word matches
            if current_word in single_word_map:
                ...
            res_word_list.append(sentence[start_position])
            start_position += 1
        dead_loop_indicator += 1
        if dead_loop_indicator > 5000:
            raise OverflowError("Maximum number of word in sentence exceeded!5000! or maybe in the dead loop!")
    return TokenSentence(segment_value=res_word_list)


def text2segment(text: str, wi: WordIndex, language_parser: LanguageParser) -> TextParagraphSegment:
    sents: Iterator[Iterable[Token]] = language_parser.split_sentences_and_tokenize(text)
    return TextParagraphSegment(segment_value=[match_word_in_sentence(sent) for sent in sents], segment_raw=text)
