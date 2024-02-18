from dataclasses import dataclass
from datetime import date, datetime

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DataclassDTO

from app.domain.books.models import Book, BookText
from app.lib import dto

__all__ = ["BookCreate", "BookCreateDTO", "BookDTO", "BookUpdate", "BookUpdateDTO", "BookTextDTO", "BookTextCreate"]


# database model


class BookDTO(SQLAlchemyDTO[Book]):
    config = dto.config(
        max_nested_depth=1,
    )


class BookTextDTO(SQLAlchemyDTO[BookText]):
    config = dto.config(exclude={"book"})


# input


@dataclass
class BookTextCreate:
    ref_book_id: int
    book_text: str


@dataclass
class BookCreate:
    book_name: str | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None
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


class BookTextCreateDTO(DataclassDTO[BookTextCreate]):
    config = dto.config()
