from dataclasses import dataclass

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DataclassDTO

from app.domain.words.models import Word
from app.lib import dto

__all__ = (
    "WordCreate",
    "WordDTO",
    "WordUpdate",
    "WordUpdateDTO",
)


# database model


class WordDTO(SQLAlchemyDTO[Word]):
    config = dto.config()


# input


@dataclass
class WordCreate:
    word_string: str
    word_lemma: str
    word_pos: str
    word_pronunciation: str | None
    word_tokens: list[str]
    word_explanation: str | None
    is_multiple_words: bool = False
    word_status: int = 0


class WordCreateDTO(DataclassDTO[WordCreate]):
    """User Create."""

    config = dto.config(exclude={"create_at", "update_at"})


@dataclass
class WordUpdate:
    word_lemma: str
    word_pos: str
    is_multiple_words: bool
    word_status: int
    word_pronunciation: str | None
    word_explanation: str | None
    word_image_path: str | None = None


class WordUpdateDTO(DataclassDTO[WordUpdate]):
    """User Update."""

    config = dto.config()


class WordPatchDTO(DataclassDTO[WordUpdate]):
    """User Update."""

    config = dto.config(partial=True)


# class BookPatchDTO(DataclassDTO[BookUpdate]):
