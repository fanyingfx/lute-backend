from collections.abc import AsyncGenerator, AsyncIterator
from pathlib import Path
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.db.models import Language
from app.db.models.book import Book
from app.db.models.word import Word
from app.server.plugins import alchemy

here = Path(__file__).parent
pytestmark = pytest.mark.anyio


@pytest.fixture(name="engine", autouse=True)
async def fx_engine() -> AsyncEngine:
    """Postgresql instance for end-to-end testing.

    Args:
        docker_ip: IP address for TCP connection to Docker containers.
        postgres_service: docker service

    Returns:
        Async SQLAlchemy engine instance.
    """
    return create_async_engine(
        url="sqlite+aiosqlite:///test1.sqlite",
        echo=False,
    )


@pytest.fixture(name="sessionmaker")
def fx_session_maker_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(name="session")
async def fx_session(sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session


@pytest.fixture(autouse=True)
async def _seed_db(
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    raw_languages: list[Language | dict[str, Any]],
    raw_books: list[Book | dict[str, Any]],
    raw_words: list[Word | dict[str, Any]],
) -> AsyncIterator[None]:
    """Populate test database with.

    Args:
        engine: The SQLAlchemy engine instance.
        sessionmaker: The SQLAlchemy sessionmaker factory.
        raw_users: Test users to add to the database
        raw_teams: Test teams to add to the database

    """

    from advanced_alchemy.base import BigIntBase

    from app.domain.book.services import BookService
    from app.domain.language.services import LanguageService
    from app.domain.word.services import WordService

    metadata = BigIntBase.registry.metadata
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    async with LanguageService.new(sessionmaker()) as language_service:
        await language_service.create_many(raw_languages, auto_commit=True)
    async with BookService.new(sessionmaker()) as book_service:
        await book_service.create_many(raw_books, auto_commit=True)
    async with WordService.new(sessionmaker()) as word_service:
        await word_service.create_many(raw_words, auto_commit=True)

    return None  # type: ignore[return-value]


@pytest.fixture(autouse=True)
def _patch_db(
    app: "Litestar",
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(alchemy._config, "session_maker", sessionmaker)
    monkeypatch.setitem(app.state, alchemy._config.engine_app_state_key, engine)
    monkeypatch.setitem(
        app.state,
        alchemy._config.session_maker_app_state_key,
        async_sessionmaker(bind=engine, expire_on_commit=False),
    )


# @pytest.fixture(name="redis")
# async def fx_redis(docker_ip: str, redis_service: None) -> Redis:
#     """Redis instance for testing.
#
#     Args:
#         docker_ip: IP of docker host.
#         redis_service: docker service
#
#     Returns:
#         Redis client instance, function scoped.
#     """


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    """Async client that calls requests on the app.

    ```text
    ValueError: The future belongs to a different loop than the one specified as the loop argument
    ```
    """
    async with AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as client:  # type: ignore[arg-type]
        yield client
