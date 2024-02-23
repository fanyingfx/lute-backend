from typing import Optional

from app.lib.db import orm

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

# how to initialize Language Model and parser
__all__ = ["Language"]


class Language(orm.DatabaseModel):
    """Language Model."""
    __tablename__ = "languages"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Language Table"}
    language_name: Mapped[str] = mapped_column(String(length=40))
    parser_name: Mapped[Optional[str]] = mapped_column(String(length=40), comment="is Right-to-left Language")
    RTL: Mapped[bool] = mapped_column(Boolean, default=False)

    # ORM Relationships
