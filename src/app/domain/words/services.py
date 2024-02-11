from __future__ import annotations

import copy
from collections import defaultdict
from typing import TYPE_CHECKING, Any

from advanced_alchemy.filters import CollectionFilter
from litestar.stores.memory import MemoryStore

from app.domain.words.models import Word
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

__all__ = ["WordService", "words_store"]

words_store = MemoryStore()


class WordIndex:
    def _init_word_list(self, word_list: list[Word]):
        word_index = defaultdict(list)
        for db_word in word_list:
            if len(db_word.word_tokens) == 0:
                raise ValueError(f"Empty word list: {db_word}")
            # using first word as key for quick search
            # I think one level is enough
            word_index[db_word.word_tokens[0]].append(copy.copy(db_word))
        # using inplace sort to sort the word list
        for key in word_index:
            word_index[key].sort(key=lambda w: w.word_counts, reverse=True)
        return word_index

    def __init__(self, word_list: list[Word]):
        self._word_index = self._init_word_list(word_list)

    def __contains__(self, key):
        return key in self._word_index

    def __getitem__(self, key) -> Word:
        return self._word_index[key]

    def __iter__(self):
        raise TypeError(f"{self.__class__.__name__!r} object is not iterable")

    def __repr__(self):
        return f"{self.__class__.__name__!r}{dict(self._word_index)!r}>"


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

    async def get_word_index(self) -> WordIndex:
        collection_filter = CollectionFilter("is_multiple_words", [True, False])
        word_list = await self.list(collection_filter)
        return WordIndex(word_list)

    async def load_word_index(self, language_name):
        if not await words_store.get(f"{language_name}-word-index-saved"):
            multiple_word_index = await self.get_word_index()
            await words_store.set(f"{language_name}-word-index", multiple_word_index)
            await words_store.set(f"{language_name}-word-index-saved", True)

    async def to_model(self, data: Word | dict[str, Any], operation: str | None = None) -> Word:
        return await super().to_model(data, operation)
