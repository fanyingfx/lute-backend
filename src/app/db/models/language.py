from advanced_alchemy.base import BigIntBase
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.parser.language_parser import LanguageParser

# from app.lib.db import orm

# how to initialize Language Model and parser
__all__ = ["Language"]


class Language(BigIntBase):
    """Language Model."""

    __tablename__ = "languages"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Language Table"}
    language_name: Mapped[str] = mapped_column(String(length=40))
    parser_name: Mapped[str] = mapped_column(String(length=40))
    RTL: Mapped[bool] = mapped_column(Boolean, default=False, comment="is Right-to-left Language")
    # book_language: Mapped["Book"] = relationship(back_populates="language", lazy="noload")
    # books: Mapped[list["Book"]] = relationship(lazy="noload", cascade="all,delete-orphan")

    def get_parser(self) -> LanguageParser:
        return LanguageParser.get_parser(self.parser_name)

        # ORM Relationships
