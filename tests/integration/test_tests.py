from typing import TYPE_CHECKING

import pytest
from httpx import AsyncClient
from litestar import get
from sqlalchemy.ext.asyncio import AsyncSession

# from app import db
from app.config import app as config

if TYPE_CHECKING:
    from litestar import Litestar
    from sqlalchemy.ext.asyncio import AsyncEngine

pytestmark = pytest.mark.anyio


# def test_cache_on_app(app: "Litestar", redis: "AsyncRedis") -> None:
#     """Test that the app's cache is patched.
#
#     Args:
#         app: The test Litestar instance
#         redis: The test Redis client instance.
#     """
#


def test_engine_on_app(app: "Litestar", engine: "AsyncEngine") -> None:
    """Test that the app's engine is patched.

    Args:
        app: The test Litestar instance
        engine: The test SQLAlchemy engine instance.
    """
    assert app.state[config.alchemy.engine_app_state_key] is engine


@pytest.mark.anyio
async def test_db_session_dependency(app: "Litestar", engine: "AsyncEngine") -> None:
    """Test that handlers receive session attached to patched engine.

    Args:
        app: The test Litestar instance
        engine: The patched SQLAlchemy engine instance.
    """

    @get("/db-session-test", opt={"exclude_from_auth": True})
    async def db_session_dependency_patched(db_session: AsyncSession) -> dict[str, str]:
        return {"result": f"{db_session.bind is engine = }"}

    app.register(db_session_dependency_patched)
    # can't use test client as it always starts its own event loop
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/db-session-test")
        assert response.json()["result"] == "db_session.bind is engine = True"
