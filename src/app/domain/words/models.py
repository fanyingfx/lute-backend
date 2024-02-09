from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.lib.db import orm

__all__ = (
    "Word",
    "WordToken",
)


class WordToken:
    word_string: str
    word_lemma: str
    word_pos: str
    is_multiple_words: bool = False
    is_word: bool = False
    is_eos: bool = False
    next_is_ws: bool = False
    word_status: int = 0


class Word(orm.DatabaseModel):
    "Word Model"
    __tablename__ = "words"
    __table_args__ = {"comment", "Words table"}

    word_string: Mapped[str] = mapped_column(String(100))
    word_lemma: Mapped[str] = mapped_column(String(100))
    word_pos: Mapped[str] = mapped_column(String(100))
    is_multiple_words: Mapped[bool] = mapped_column(Boolean)
    is_word: Mapped[bool] = mapped_column(Boolean)
    is_eos: Mapped[bool] = mapped_column(Boolean)
    word_status: Mapped[int] = mapped_column(Integer)
    pronunciation: Mapped[str] = mapped_column(String(100))
    explanation: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
