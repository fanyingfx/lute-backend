from dataclasses import dataclass
from datetime import date
from datetime import datetime

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DataclassDTO

from app.domain.books.models import Book
from app.lib import dto

__all__ = [
    "BookCreate",
    "BookCreateDTO",
    "BookDTO",
    "BookUpdate",
    "BookUpdateDTO",
]


# database model


class BookDTO(SQLAlchemyDTO[Book]):
    config = dto.config(
        max_nested_depth=1,
    )


# input


@dataclass
class BookCreate:
    book_name: str | None = None
    create_at: datetime = None
    update_at: datetime = None
    published_at: date|None = None


class BookCreateDTO(DataclassDTO[BookCreate]):
    """User Create."""

    config = dto.config(exclude={"create_at", "update_at"})



@dataclass
class BookUpdate:
    book_name: str | None = None
    published_at: date|None =None

class BookUpdateDTO(DataclassDTO[BookUpdate]):
    """User Update."""
    config = dto.config()

class BookPatchDTO(DataclassDTO[BookUpdate]):
    config = dto.config(partial=True)
