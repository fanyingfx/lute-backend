from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib.db import orm

__all__ = ("Word",)


class Word(orm.DatabaseModel):
    "Word Model"
    __tablename__ = "words"
    __table_args__ = {"comment": "Words table"}

    word_string: Mapped[str] = mapped_column(String(100))
    word_lemma: Mapped[str | None] = mapped_column(String(100))
    word_pos: Mapped[str | None] = mapped_column(String(100))
    is_multiple_words: Mapped[bool] = mapped_column(Boolean)
    word_status: Mapped[int] = mapped_column(Integer)
    word_pronunciation: Mapped[str | None] = mapped_column(String(100))
    word_explanation: Mapped[str | None] = mapped_column(String(100))
    word_counts: Mapped[int | None] = mapped_column(Integer)
    word_tokens: Mapped[list[str]] = mapped_column(orm.JSONType)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    word_image: Mapped[WordImage | None] = relationship(lazy="noload", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Word(word_string={self.word_string}, word_lemma={self.word_lemma},word_pos={self.word_pos},"
            f"is_multiple_words={self.is_multiple_words},word_status={self.word_status},word_pronunciation={self.word_pronunciation}"
            f"word_explanation={self.word_explanation},word_counts={self.word_tokens},word_tokens={self.word_tokens})>"
        )

    UniqueConstraint(word_string)


class WordImage(orm.DatabaseModel):
    __tablename__ = "word_images"
    word_id: Mapped[str] = mapped_column(ForeignKey("words.id"))
    word_image_name: Mapped[str] = mapped_column(String(100))
    word_image_path: Mapped[str] = mapped_column(String(100))
    word: Mapped[Word] = relationship(back_populates="word_image", lazy="noload")
