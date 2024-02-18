from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib.db import orm

__all__ = ["Book", "BookText"]


class Book(orm.DatabaseModel):
    """Book Model."""

    __tablename__ = "books"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    book_name: Mapped[str] = mapped_column(String(length=300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()  # type: ignore[arg-type]
    )
    published_at: Mapped[date | None] = mapped_column(Date())

    # ORM Relationships
    texts: Mapped[list[BookText]] = relationship(lazy="noload", cascade="all,delete-orphan")


class BookText(orm.DatabaseModel):
    __tablename__ = "booktexts"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic BookText Table"}
    ref_book_id: Mapped[Integer] = mapped_column(ForeignKey("books.id"))
    book_text: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"BookText(id={self.id!r}, book_text={self.book_text!r})"

    book: Mapped[Book] = relationship(back_populates="texts", lazy="noload")
