from dataclasses import dataclass

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DataclassDTO

from app.db.models.language import Language
from app.lib import dto

__all__ = ["LanguageDTO", "LanguageData", "LanguageCreateDTO", "LanguageUpdateDTO", "LanguagePatchDTO"]


# database model


class LanguageDTO(SQLAlchemyDTO[Language]):
    config = dto.config()


@dataclass
class LanguageData:
    language_name: str
    parser_name: str
    RTL: bool = False


class LanguageCreateDTO(DataclassDTO[LanguageData]):
    """User Create."""

    config = dto.config()


class LanguageUpdateDTO(DataclassDTO[LanguageData]):
    """User Update."""

    config = dto.config()


class LanguagePatchDTO(DataclassDTO[LanguageData]):
    config = dto.config(partial=True)
