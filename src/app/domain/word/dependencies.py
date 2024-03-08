"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload, noload

from app.domain.word.services import WordService

__all__ = ["provides_word_service"]

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provides_word_service(db_session: AsyncSession) -> AsyncGenerator[WordService, None]:
    """Construct repository and service objects for the request."""
    from app.db.models.word import Word

    async with WordService.new(
        session=db_session,
        statement=select(Word)
        .options(joinedload(Word.language))
        .options(
            joinedload(Word.word_image),
            noload("*"),
        ),
    ) as service:
        yield service
