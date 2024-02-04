from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib.db import orm

__all__ = ["Book", "BookText"]


class Book(orm.DatabaseModel):
    """Book Model."""

    __tablename__ = "book"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    book_name: Mapped[str] = mapped_column(String(length=300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    published_at: Mapped[date | None] = mapped_column(Date())

    # ORM Relationships
    texts: Mapped[list[BookText]] = relationship(back_populates="book", cascade="all,delete-orphan")

    def __init__(self, book_name: str, published_at: date | None = None):
        self.book_name = book_name
        self.published_at = published_at

    def __repr__(self):
        return (
            f"Book(id={self.id!r}, book_name={self.book_name!r},"
            f" created_at={self.created_at!r}, updated_at={self.updated_at!r}"
        )


class BookText(orm.DatabaseModel):
    __tablename__ = "booktext"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    ref_book_id: Mapped[Integer] = mapped_column(ForeignKey("book.id"))
    # book: Mapped[Book] = relationship(
    book_text: Mapped[str] = mapped_column(Text)
    book: Mapped[Book] = relationship(back_populates="texts")
