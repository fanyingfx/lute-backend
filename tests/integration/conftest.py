from collections.abc import AsyncGenerator, AsyncIterator
from pathlib import Path
from typing import Any

import pytest
from httpx import AsyncClient
from litestar import Litestar
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.domain.books.models import Book
from app.lib import db

here = Path(__file__).parent
pytestmark = pytest.mark.anyio


@pytest.fixture(name="engine")
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
    raw_books: list[Book | dict[str, Any]],
    # raw_teams: list[Team | dict[str, Any]],
) -> AsyncIterator[None]:
    """Populate test database with.

    Args:
        engine: The SQLAlchemy engine instance.
        sessionmaker: The SQLAlchemy sessionmaker factory.
        raw_users: Test users to add to the database
        raw_teams: Test teams to add to the database

    """

    from app.domain.books.services import BookService
    from app.lib.db import orm  # pylint: disable=[import-outside-toplevel,unused-import]

    metadata = orm.DatabaseModel.registry.metadata
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    async with BookService.new(sessionmaker()) as users_service:
        await users_service.create_many(raw_books)
        await users_service.repository.session.commit()
    # async with TeamService.new(sessionmaker()) as teams_services:
    #     for raw_team in raw_teams:

    return None  # type: ignore[return-value]


@pytest.fixture(autouse=True)
def _patch_db(
    app: "Litestar",
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(db, "async_session_factory", sessionmaker)
    monkeypatch.setattr(db.base, "async_session_factory", sessionmaker)
    monkeypatch.setitem(app.state, db.config.engine_app_state_key, engine)
    monkeypatch.setitem(
        app.state,
        db.config.session_maker_app_state_key,
        async_sessionmaker(bind=engine, expire_on_commit=False),
    )


@pytest.fixture(name="redis")
async def fx_redis(docker_ip: str, redis_service: None) -> Redis:
    """Redis instance for testing.

    Args:
        docker_ip: IP of docker host.
        redis_service: docker service

    Returns:
        Redis client instance, function scoped.
    """
    return Redis(host=docker_ip, port=6397)


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    """Async client that calls requests on the app.

    ```text
    ValueError: The future belongs to a different loop than the one specified as the loop argument
    ```
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
