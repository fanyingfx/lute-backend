"""Language Service."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from app.domain.language.models import Language
from app.domain.language.services import LanguageService

__all__ = ["provides_language_service"]

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provides_language_service(db_session: AsyncSession) -> AsyncGenerator[LanguageService, None]:
    """Construct repository and service objects for the request."""
    async with LanguageService.new(session=db_session, statement=select(Language)) as service:
        yield service
