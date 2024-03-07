from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from litestar.repository.filters import CollectionFilter, OrderBy

from app.db.models.word import Word
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

__all__ = ["WordService"]


# words_store = MemoryStore()


# @listener("word_created", "word_updated", "word_deleted")
# async def on_word_updated(language_name: str, word_string: str = "") -> None:
#     await words_store.delete(f"{language_name}-word-index-saved")
# await WordService.update_word_index(language_name, word_string)

#
# class WordIndex:
#     def _init_word_list(self, word_list: Sequence[Word]) -> dict[str, list[Word]]:
#         word_index: dict[str, list[Word]] = defaultdict(list)
#         for db_word in word_list:
#             if len(db_word.word_tokens) == 0:
#                 raise ValueError(f"Empty word list: {db_word}")
#             # using first word as key for quick search
#             # I think one level is enough
#             word_index[db_word.first_word].append(copy.copy(db_word))
#         # using inplace sort to sort the word list
#         for key in word_index:
#             word_index[key].sort(key=lambda w: w.word_counts, reverse=True)  # type: ignore
#         return word_index
#
#     def __init__(self, word_list: Sequence[Word]):
#         self._word_index = self._init_word_list(word_list)
#
#     def __contains__(self, key: str) -> bool:
#         return key in self._word_index
#
#     def __getitem__(self, key: str) -> Sequence[Word]:
#         return self._word_index[key]
#
#     def __setitem__(self, key: str, value: list[Word]) -> None:
#         self._word_index[key] = value
#
#     def __iter__(self) -> NoReturn:
#         raise TypeError(f"{self.__class__.__name__!r} object is not iterable")
#
#     def __repr__(self) -> str:
#         return f"{self.__class__.__name__!r}{dict(self._word_index)!r}>"


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
        word_list = await self.list(
            CollectionFilter("language_id", [language_id]),
            CollectionFilter("first_word", [word_string]),
            OrderBy("word_counts", "desc"),
        )

        self.word_index[language_id][word_string] = list(word_list)

    async def to_model(self, data: Word | dict[str, Any], operation: str | None = None) -> Word:
        return await super().to_model(data, operation)
