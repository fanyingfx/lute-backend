from dataclasses import dataclass
from datetime import date, datetime

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DataclassDTO

from app.db.models.book import Book, BookText
from app.domain.parser.markdown_text_parser import BaseSegment, ParsedTextSegment
from app.lib import dto

__all__ = [
    "BookCreate",
    "BookCreateDTO",
    "BookDTO",
    "BookUpdate",
    "BookUpdateDTO",
    "BookTextDTO",
    "BookTextCreate",
    "BaseSegment",
    "ParsedTextSegment",
    "ParsedBookTextDTO",
    "ParsedBookText",
]

# database model

from dataclasses import dataclass

# T = TypeVar("T")

# @dataclass
# class ReturnData(Generic[T]):
#     data: list[T]


@dataclass
class ParsedBookText:
    data: list[ParsedTextSegment]


class ParsedBookTextDTO(DataclassDTO[ParsedBookText]):
    config = dto.config(
        max_nested_depth=4,
    )


class BookDTO(SQLAlchemyDTO[Book]):
    config = dto.config(
        max_nested_depth=1,
    )


class BookTextDTO(SQLAlchemyDTO[BookText]):
    config = dto.config(exclude={"book"})


# input


@dataclass
class BookTextCreate:
    book_text: str
    book_title: str | None = None


@dataclass
class BookCreate:
    language_id: int
    book_name: str | None = None
    create_at: datetime = None
    update_at: datetime = None
    published_at: date | None = None
    texts: list[BookTextCreate] | None = None


# class BookParsedDTO(DataclassDTO[Segment]):
#     config = dto.config()


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
