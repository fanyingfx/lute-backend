from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

from .models import Word

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

__all__ = ["WordService"]


class WordRepository(SQLAlchemyAsyncRepository[Word]):
    """Word SQLAlchemy Repository."""

    model_type = Word


class WordService(SQLAlchemyAsyncRepositoryService[Word]):
    """Handles database operations for users."""

    repository_type = WordRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: WordRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(self, data: Word | dict(str, Any)) -> Word:
        # if isinstance(data, dict) and 'word_tokens' in data:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=True)

    async def update(
        self,
        data: Word | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> Word:
        return await super().update(item_id=item_id, data=data, auto_commit=True)

    async def to_model(self, data: Word | dict[str, Any], operation: str | None = None) -> Word:
        return await super().to_model(data, operation)
