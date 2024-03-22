from dataclasses import dataclass
from datetime import date

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.contrib.pydantic import PydanticDTO
from litestar.datastructures import UploadFile
from litestar.dto import DataclassDTO
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

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
    "BookPatchDTO",
    "BookTextCreateDTO",
]


@dataclass
class ParsedBookText:
    data: list[ParsedTextSegment]


class ParsedBookTextDTO(DataclassDTO[ParsedBookText]):
    config = dto.config(
        max_nested_depth=4,
    )


class BookDTO(SQLAlchemyDTO[Book]):
    config = dto.config(max_nested_depth=1, exclude={"texts.0.ref_book_id", "texts.0.book_text"})


class BookTextDTO(SQLAlchemyDTO[BookText]):
    config = dto.config(exclude={"book"})


# input


@dataclass
class BookTextCreate:
    book_text: str
    book_title: str | None = None


class BookCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel)
    file: UploadFile
    language_id: int
    book_name: str | None = Field(default=True)
    # create_at: datetime | None = Field(default=None)
    # update_at: datetime | None = Field(default=None)
    # published_at: date | None = Field(default=None)


# class BookParsedDTO(DataclassDTO[Segment]):
#     config = dto.config()


class BookCreateDTO(PydanticDTO[BookCreate]):
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
