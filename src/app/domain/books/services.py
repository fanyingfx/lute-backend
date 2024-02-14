from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from app.domain.books.models import Book, BookText
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService
from app.parsers.MarkdownTextParser import TextParagraphSegment, TokenSentence, VWord

if TYPE_CHECKING:
    from collections.abc import Iterable

    from spacy.tokens import Token
    from sqlalchemy.orm import InstrumentedAttribute

    from app.domain.words.models import Word
    from app.domain.words.services import WordIndex
    from app.parsers.language_parsers.LanguageParser import LanguageParser

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


def find_in_multiple_words(word_token, word_list: list[Word]):
    pass


async def match_word_in_sentence(sentence: Iterable[Token], word_index: WordIndex, max_loop_num: int) -> TokenSentence:
    start_position = 0
    res_word_list = []
    dead_loop_indicator = 0
    sentence_length = len(sentence)

    while start_position < sentence_length:
        current_word = str(sentence[start_position])
        current_token: Token = sentence[start_position]
        vword = VWord(
            word_string=current_token.text,
            word_lemma=current_token.lemma_,
            word_pos=current_token.pos_,
            is_multiple_words=False,
            is_word=not current_token.is_punct,
            is_eos=current_token.is_sent_end,
            next_is_ws=" " in current_token.text_with_ws,
            word_status=0,
            word_explanation="",
            word_pronunciation="",
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
                    vword.word_lemma = db_word.word_lemma
                    vword.word_pos = db_word.word_pos
                    vword.is_multiple_words = db_word.is_multiple_words
                    vword.is_word = True
                    vword.is_eos = sentence[end_position].is_sent_end
                    vword.next_is_ws = " " in sentence[end_position].text_with_ws
                    vword.word_status = db_word.word_status
                    vword.word_explanation = db_word.word_explanation
                    vword.word_pronunciation = db_word.word_pronunciation
                    start_position = end_position
                    break
        res_word_list.append(vword)

        start_position += 1
        dead_loop_indicator += 1
        if dead_loop_indicator > max_loop_num:
            raise OverflowError(
                f"Maximum number of word in sentence exceeded !{max_loop_num}! or maybe in the dead loop!"
            )
    return TokenSentence(segment_value=res_word_list)


async def text2segment(text: str, language_parser: LanguageParser) -> TextParagraphSegment:
    """
    Returns:
        object: TextParagraphSegment
    """
    sents: Iterator[Iterable[Token]] = language_parser.split_sentences_and_tokenize(text)
    max_loop_num = len(text) * 100
    from app.domain.words.services import words_store

    language_name = language_parser.get_language_name()
    word_index: WordIndex = await words_store.get(f"{language_name}-word-index")
    sentences = []
    for sent in sents:
        parsed_sent = await match_word_in_sentence(sent, word_index, max_loop_num)
        sentences.append(parsed_sent)
    return TextParagraphSegment(segment_value=sentences, segment_raw=text)
