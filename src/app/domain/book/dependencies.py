"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload, noload, selectinload

from app.db.models.book import Book, BookText
from app.domain.book.services import BookService, BookTextService

__all__ = [
    "provides_book_service",
]

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provides_book_service(db_session: AsyncSession) -> AsyncGenerator[BookService, None]:
    """Construct repository and service objects for the request."""
    async with BookService.new(
        session=db_session,
        statement=select(Book)
        .options(
            selectinload(Book.texts).options(
                joinedload(BookText.book).options(noload("*")),
            ),
            noload("*"),
        )
        .options(joinedload(Book.language)),
        # .join(BookText, onclause=Book.id == BookText.ref_book_id, isouter=True)
        # .order_by(Book.updated_at)
        # .options(
        # ),
    ) as service:
        yield service


async def provides_booktext_service(db_session: AsyncSession) -> AsyncGenerator[BookTextService, None]:
    """Construct repository and service objects for the request."""
    async with BookTextService.new(
        session=db_session,
        statement=select(BookText).options(joinedload(BookText.book).options(joinedload(Book.language))),
    ) as service:
        yield service
