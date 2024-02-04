from __future__ import annotations

from datetime import date
from datetime import datetime  # noqa: TCH003
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String, Date
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib import dto
from app.lib.db import orm

__all__ = ["Book","BookText"]


class Book(orm.DatabaseModel):
    """Book Model."""

    __tablename__ = "book"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    # id: Mapped[int] = mapped_column(primary_key=True)
    book_name: Mapped[str] = mapped_column(String(length=300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 server_onupdate=func.now())
    published_at: Mapped[date | None] = mapped_column(Date())

    # ORM Relationships
    texts : Mapped[list[BookText]] = relationship(back_populates="book")


    def __init__(self, book_name: str, published_at: date = None):
        self.book_name = book_name
        self.published_at = published_at

    # is_superuser: Mapped[bool] = mapped_column(default=False)
    # is_verified: Mapped[bool] = mapped_column(default=False)
    # verified_at: Mapped[datetime | None] = mapped_column(info=dto.dto_field("read-only"))
    # -----------
    # ORM Relationships
    # ------------
    # texts: Mapped[list[BookText]]= relationship(back_populates="book",
    #                                              cascade="all, delete",
    #                                              lazy="noload",
    #                                              passive_deletes=True,
    #                                              )
    # texts : Mapped[list['BookText']] = relationship(back_populates="book")


    def __repr__(self):
        return f"Book(id={self.id!r}, book_name={self.book_name!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r}"

class BookText(orm.DatabaseModel):
    __tablename__ = "booktext"  # type: ignore[assignment]
    __table_args__ = {"comment": "Basic Book Table"}
    ref_book_id: Mapped[Integer] = mapped_column(ForeignKey("book.id"))
    # book: Mapped[Book] = relationship(
    #     back_populates="texts",
    #     foreign_keys="BookText.ref_book_id",
    #     innerjoin=True,
    #     uselist=False,
    #     lazy="noload",
    # )
    book_text: Mapped[str] = mapped_column(Text)
    book: Mapped[Book] = relationship(back_populates="texts")
    # book: Mapped['Book'] = relationship(back_populates="texts")
    # book: Mapped[Book] = relationship(back_populates="texts")

