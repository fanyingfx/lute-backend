from dataclasses import dataclass
from datetime import date, datetime

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DataclassDTO

from app.domain.words.models import Word
from app.lib import dto

__all__ = (
    "BookCreate",
    "BookCreateDTO",
    "BookPatchDTO",
    "BookUpdate",
    "BookUpdateDTO",
    "WordCreate",
    "WordDTO",
)


# database model


class WordDTO(SQLAlchemyDTO[Word]):
    config = dto.config()


# input


@dataclass
class WordCreate:
    ref_book_id: int
    book_text: str


@dataclass
class BookCreate:
    book_name: str | None = None
    create_at: datetime = None
    update_at: datetime = None
    published_at: date | None = None
    text: str | None = None


class BookCreateDTO(DataclassDTO[BookCreate]):
    """User Create."""

    config = dto.config(exclude={"create_at", "update_at"})


@dataclass
class BookUpdate:
    book_name: str | None = None
    published_at: date | None = None


class BookUpdateDTO(DataclassDTO[BookUpdate]):
    """User Update."""

    config = dto.config()


class BookPatchDTO(DataclassDTO[BookUpdate]):
    config = dto.config(partial=True)
