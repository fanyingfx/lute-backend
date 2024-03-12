from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntBase
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ("Word", "WordImage")

from app.db.models.base import JSONType

if TYPE_CHECKING:
    from app.db.models.language import Language


class Word(BigIntBase):
    "Word Model"
    __tablename__ = "words"  # type: ignore[assignment]
    __table_args__ = {"comment": "Words table"}

    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    word_string: Mapped[str] = mapped_column(String(100))
    word_lemma: Mapped[str | None] = mapped_column(String(100))
    word_pos: Mapped[str | None] = mapped_column(String(100))
    is_multiple_words: Mapped[bool] = mapped_column(Boolean)
    word_status: Mapped[int] = mapped_column(Integer)
    word_pronunciation: Mapped[str | None] = mapped_column(String(100))
    word_explanation: Mapped[str | None] = mapped_column(String(100))
    word_counts: Mapped[int | None] = mapped_column(Integer)
    word_tokens: Mapped[list[str]] = mapped_column(JSONType)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()  # type: ignore
    )
    first_word: Mapped[str] = mapped_column(String(100))
    language: Mapped["Language"] = relationship(lazy="joined")  # noqa
    word_image: Mapped[WordImage] = relationship(lazy="joined", cascade="all, delete, delete-orphan")

    UniqueConstraint(word_string)


class WordImage(BigIntBase):
    __tablename__ = "word_images"  # type: ignore[assignment]
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    word_image_name: Mapped[str] = mapped_column(String(100))
    word_image_path: Mapped[str] = mapped_column(String(100))
    word: Mapped[Word] = relationship(back_populates="word_image", lazy="joined", single_parent=True)
    __table_args__ = (UniqueConstraint("word_id"),)
