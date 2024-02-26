from __future__ import annotations

from datetime import date, datetime

from advanced_alchemy.base import BigIntBase
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["Book", "BookText"]


class Book(BigIntBase):
    """Book Model."""

    __tablename__ = "books"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    book_name: Mapped[str] = mapped_column(String(length=300))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    published_at: Mapped[date | None] = mapped_column(Date())

    # ORM Relationships
    texts: Mapped[list[BookText]] = relationship(lazy="noload", cascade="all,delete-orphan")

    # def __init__(self, book_name: str, published_at: date | None = None, **kw: Any):

    def __repr__(self):
        return (
            f"Book(id={self.id!r}, book_name={self.book_name!r},"
            f" created_at={self.created_at!r}, updated_at={self.updated_at!r})"
        )


class BookText(BigIntBase):
    __tablename__ = "booktexts"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic BookText Table"}
    ref_book_id: Mapped[Integer] = mapped_column(ForeignKey("books.id"))
    # book: Mapped[Book] = relationship(
    book_text: Mapped[str] = mapped_column(Text)

    def __init__(self, ref_book_id: int, book_text: str):
        self.ref_book_id = ref_book_id
        self.book_text = book_text

    def __repr__(self):
        return f"BookText(id={self.id!r}, book_text={self.book_text!r})"

    book: Mapped[Book] = relationship(back_populates="texts", lazy="noload")
