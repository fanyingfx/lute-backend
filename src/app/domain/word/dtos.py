from dataclasses import dataclass

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.datastructures import UploadFile
from litestar.dto import DataclassDTO
from pydantic import BaseConfig, BaseModel, Field

from app.db.models.word import Word
from app.lib import dto

__all__ = ("WordCreate", "WordDTO", "WordUpdate", "WordUpdateDTO", "WordImageFormData")


# database model


class WordDTO(SQLAlchemyDTO[Word]):
    config = dto.config(exclude={"word_image", "first_word"}, max_nested_depth=1, rename_fields={"id": "wordDbId"})


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


@dataclass(kw_only=True)
class WordUpdate:
    word_string: str
    language_id: int
    word_lemma: str = ""
    word_pos: str = ""
    word_status: int
    is_multiple_words: bool = False
    word_pronunciation: str | None = None
    word_explanation: str | None = None
    word_image_path: str | None = None
    word_tokens: list[str]
    word_counts: int
    # id:int


class WordUpdateDTO(DataclassDTO[WordUpdate]):
    """User Update."""

    config = dto.config()


class WordPatchDTO(DataclassDTO[WordUpdate]):
    """User Update."""

    config = dto.config(partial=True)


class WordImageFormData(BaseModel):
    word_image_file: UploadFile
    save_local: bool = Field(default=True)
    word_id: int | None = Field(default=None)
    word_image_name: str | None = Field(default=None)

    class Config(BaseConfig):
        arbitrary_types_allowed = True


# class BookPatchDTO(DataclassDTO[BookUpdate]):
