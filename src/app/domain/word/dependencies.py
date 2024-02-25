"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import noload

from app.domain.word.services import WordService

__all__ = ["provides_word_service"]


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provides_word_service(db_session: AsyncSession) -> AsyncGenerator[WordService, None]:
    """Construct repository and service objects for the request."""
    from app.domain.word.models import Word

    async with WordService.new(
        session=db_session,
        statement=select(Word).options(
            #     options(
            # selectinload(Word.word_image).options(
            # ),
            noload("*")
        ),
    ) as service:
        yield service
