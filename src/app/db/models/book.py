from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntBase
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["Book", "BookText"]
if TYPE_CHECKING:
    from app.db.models.language import Language


class Book(BigIntBase):
    """Book Model."""

    __tablename__ = "books"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    book_name: Mapped[str] = mapped_column(String(length=300))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()  # type: ignore[arg-type]
    )
    published_at: Mapped[date | None] = mapped_column(Date())

    # ORM Relationships
    texts: Mapped[list[BookText]] = relationship(cascade="all,delete-orphan")
    language: Mapped["Language"] = relationship(lazy="noload")  # noqa


class BookText(BigIntBase):
    __tablename__ = "booktexts"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic BookText Table"}
    ref_book_id: Mapped[Integer] = mapped_column(ForeignKey("books.id"))
    title: Mapped[str] = mapped_column(String(length=300), nullable=True)
    book_text: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"BookText(id={self.id!r}, book_text={self.book_text!r}, title={self.title!r})"
