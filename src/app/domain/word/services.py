from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from litestar.repository.filters import CollectionFilter, OrderBy

from app.db.models.word import Word, WordImage
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

__all__ = ["WordService", "WordImageService"]


class WordRepository(SQLAlchemyAsyncRepository[Word]):
    """Word SQLAlchemy Repository."""

    model_type = Word


class WordService(SQLAlchemyAsyncRepositoryService[Word]):
    """Handles database operations for users."""

    repository_type = WordRepository
    word_index: dict[int, dict[str, list[Word]]] = {}

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: WordRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(
        self,
        data: Word | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> Word:
        # if isinstance(data, dict) and 'word_tokens' in data:
        if isinstance(data, dict):
            data["first_word"] = data["word_tokens"][0]
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def create_or_update(self, data: dict[str, Any]) -> Word:
        db_obj: Word | None = await self.get_one_or_none(word_string=data["word_string"])
        if db_obj is None:
            return await self.create(data)
        return await super().update(item_id=db_obj.id, data=data, auto_commit=True)

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
        db_obj: Word = await self.to_model(data, "update")
        return await super().update(item_id=item_id, data=db_obj, auto_commit=True)

    async def get_word_index(self, language_id: int) -> dict[str, list[Word]]:
        if language_id not in self.word_index:
            self.word_index[language_id] = defaultdict(list)
        word_list = await self.list(CollectionFilter("language_id", [language_id]), OrderBy("word_counts", "desc"))
        for word in word_list:
            self.word_index[language_id][word.first_word].append(word)
        return self.word_index[language_id]

    async def load_word_index(self, language_id: int) -> dict[str, list[Word]]:
        if language_id not in self.word_index:
            return await self.get_word_index(language_id)
        return self.word_index[language_id]

    async def update_word_index(self, language_id: int, word_string: str) -> None:
        if language_id not in self.word_index:
            return
        word_list = await self.list(
            CollectionFilter("language_id", [language_id]),
            CollectionFilter("first_word", [word_string]),
            OrderBy("word_counts", "desc"),
        )
        if not word_list:
            del self.word_index[language_id][word_string]
            return

        self.word_index[language_id][word_string] = list(word_list)

    async def to_model(self, data: Word | dict[str, Any], operation: str | None = None) -> Word:
        return await super().to_model(data, operation)


class WordImageRepository(SQLAlchemyAsyncRepository[WordImage]):
    """Word SQLAlchemy Repository."""

    model_type = WordImage


class WordImageService(SQLAlchemyAsyncRepositoryService[WordImage]):
    """Handles database operations for users."""

    repository_type = WordImageRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: WordImageRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(
        self,
        data: WordImage | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> WordImage:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def update(
        self,
        data: WordImage | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> WordImage:
        db_obj = await self.to_model(data, "update")
        return await super().update(item_id=item_id, data=db_obj, auto_commit=True)

    async def delete(
        self,
        item_id: Any,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> WordImage:
        return await super().delete(item_id=item_id, auto_commit=auto_commit)
