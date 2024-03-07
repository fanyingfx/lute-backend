from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.db.models.book import Book, BookText
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

    from app.domain.book.dtos import BookTextCreate

__all__ = ["BookService", "BookTextService"]


class BookRepository(SQLAlchemyAsyncRepository[Book]):
    """Book SQLAlchemy Repository."""

    model_type = Book


class BookTextRepository(SQLAlchemyAsyncRepository[BookText]):
    """BookText SQLAlchemy Repository."""

    model_type = BookText


class BookService(SQLAlchemyAsyncRepositoryService[Book]):
    """Handles database operations for users."""

    repository_type = BookRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: BookRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create_with_contents(self, data: Book | dict[str, Any], contents: list[BookTextCreate]) -> Book:
        book_obj = await self.to_model(data, "create")
        book = await super().create(data=book_obj, auto_commit=False)
        for content in contents:
            book.texts.append(BookText(ref_book_id=book.id, book_text=content.book_text, title=content.book_title))
        return await self.update(item_id=book.id, data=book)

    async def create(
        self,
        data: Book | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> Book:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def update(
        self,
        data: Book | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> Book:
        return await super().update(item_id=item_id, data=data, auto_commit=True)

    async def update_bookname(self, data: dict[str, Any], db_obj: Book) -> None:
        """Update stored user password.

        This is only used when not used IAP authentication.
        """
        db_obj.book_name = data.get("book_name")  # type: ignore[assignment]
        await self.repository.update(db_obj)

    async def to_model(self, data: Book | dict[str, Any], operation: str | None = None) -> Book:
        return await super().to_model(data, operation)


class BookTextService(SQLAlchemyAsyncRepositoryService[BookText]):
    """Handles database operations for users."""

    repository_type = BookTextRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: BookTextRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(
        self,
        data: BookText | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> BookText:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def update(
        self,
        data: BookText | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> BookText:
        db_obj = await self.to_model(data, "update")
        return await super().update(item_id=item_id, data=db_obj, auto_commit=auto_commit)

    async def to_model(self, data: BookText | dict[str, Any], operation: str | None = None) -> BookText:
        return await super().to_model(data, operation)
