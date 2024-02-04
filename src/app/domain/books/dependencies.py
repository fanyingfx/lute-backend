"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload, noload, selectinload

from app.domain.books.models import Book, BookText
from app.domain.books.services import BookService

__all__ = ["provides_book_service"]


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provides_book_service(db_session: AsyncSession) -> AsyncGenerator[Book, None]:
    """Construct repository and service objects for the request."""
    async with BookService.new(
        session=db_session,
        statement=select(Book)
        .join(BookText, onclause=Book.id == BookText.ref_book_id, isouter=True)
        .options(
            selectinload(Book.texts).options(
                joinedload(BookText.book, innerjoin=True).options(noload("*")),
            ),
            noload("*"),
        ),
        # .order_by(Book.updated_at)
        # .options(
        # ),
    ) as service:
        yield service
