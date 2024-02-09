from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

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
    word_tokens: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
