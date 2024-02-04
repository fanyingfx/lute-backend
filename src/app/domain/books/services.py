from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService

from .models import Book

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy.orm import InstrumentedAttribute

__all__ = ["BookService"]


class BookRepository(SQLAlchemyAsyncRepository[Book]):
    """Book SQLAlchemy Repository."""

    model_type = Book


class BookService(SQLAlchemyAsyncRepositoryService[Book]):
    """Handles database operations for users."""

    repository_type = BookRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: BookRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(self, data: Book | dict(str, Any)) -> Book:
        db_obj = await self.to_model(data, "create")
        return await super().create(data=db_obj, auto_commit=True)

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
        db_obj.book_name = data.get("book_name")
        await self.repository.update(db_obj)

    # async def get_book_by_id(self, id: int) -> Book:
    #         select(Book).join(BookText, onclause=Book.id == BookText.ref_book_id, isouter=False).options(
    #             selectinload(
    #                 Book.texts).options(
    #                 joinedload(
    #                     BookText.book
    #                     ,
    #                     noload(
    #                         "*")),
    #             ),
    #             noload("*"))
    #     ).execution_options(populate_existing=True)

    async def to_model(self, data: Book | dict[str, Any], operation: str | None = None) -> Book:
        return await super().to_model(data, operation)
