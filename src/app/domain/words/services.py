from __future__ import annotations

import copy
from collections import defaultdict
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, NoReturn

from litestar.events import listener
from litestar.stores.memory import MemoryStore

from app.domain.words.models import Word
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

__all__ = ["WordService", "words_store"]

words_store = MemoryStore()


@listener("word_created", "word_updated")
async def on_word_updated(language_name: str) -> None:
    await words_store.delete(f"{language_name}-word-index-saved")


class WordIndex:
    def _init_word_list(self, word_list: Sequence[Word]) -> dict[str, list[Word]]:
        word_index: dict[str, list[Word]] = defaultdict(list)
        for db_word in word_list:
            if len(db_word.word_tokens) == 0:
                raise ValueError(f"Empty word list: {db_word}")
            # using first word as key for quick search
            # I think one level is enough
            word_index[db_word.word_tokens[0]].append(copy.copy(db_word))
        # using inplace sort to sort the word list
        for key in word_index:
            word_index[key].sort(key=lambda w: w.word_counts, reverse=True)  # type: ignore
        return word_index

    def __init__(self, word_list: Sequence[Word]):
        self._word_index = self._init_word_list(word_list)

    def __contains__(self, key: str) -> bool:
        return key in self._word_index

    def __getitem__(self, key: str) -> list[Word]:
        return self._word_index[key]

    def __iter__(self) -> NoReturn:
        raise TypeError(f"{self.__class__.__name__!r} object is not iterable")

    def __repr__(self) -> str:
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

    async def create(
        self,
        data: Word | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> Word:
        # if isinstance(data, dict) and 'word_tokens' in data:
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

    async def get_word_index(self) -> WordIndex:
        word_list = await self.list()
        return WordIndex(word_list)

    async def load_word_index(self, language_name: str) -> None:
        if not await words_store.get(f"{language_name}-word-index-saved"):
            word_index = await self.get_word_index()
            await words_store.set(f"{language_name}-word-index", word_index)  # type: ignore
            await words_store.set(f"{language_name}-word-index-saved", True)  # type: ignore

    async def to_model(self, data: Word | dict[str, Any], operation: str | None = None) -> Word:
        return await super().to_model(data, operation)
