"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from app.domain.words.services import WordService

__all__ = ["provides_word_service"]


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provides_word_service(db_session: AsyncSession) -> AsyncGenerator[WordService, None]:
    """Construct repository and service objects for the request."""
    from app.domain.words.models import Word

    async with WordService.new(session=db_session, statement=select(Word)) as service:
        yield service
