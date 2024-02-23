from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock

import pytest
from structlog.contextvars import clear_contextvars
from structlog.testing import CapturingLogger

from app.domain.words.models import Word

if TYPE_CHECKING:
    from collections import abc

    from litestar import Litestar
    from pytest import FixtureRequest, MonkeyPatch

    from app.domain.book.models import Book

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop() -> abc.Iterator[asyncio.AbstractEventLoop]:
    """Scoped Event loop.

    Need the event loop scoped to the session so that we can use it to check
    containers are ready in session scoped containers fixture.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


def pytest_addoption(parser: pytest.Parser) -> None:
    """Adds Pytest ini config variables for the plugin."""
    parser.addini(
        "unit_test_pattern",
        (
            "Regex used to identify if a test is running as part of a unit or integration test "
            "suite. The pattern is matched against the path of each test function and affects the "
            "behavior of fixtures that are shared between unit and integration tests."
        ),
        type="string",
        default=r"^.*/tests/unit/.*$",
    )


@pytest.fixture(name="app")
def fx_app(pytestconfig: pytest.Config, monkeypatch: MonkeyPatch) -> Litestar:
    """App fixture.

    Returns:
        An application instance, configured via plugin.
    """
    from app.asgi import create_app

    return create_app(debug=False)


@pytest.fixture(name="is_unit_test")
def fx_is_unit_test(request: FixtureRequest) -> bool:
    """Uses the ini option `unit_test_pattern` to determine if the test is part
    of unit or integration tests.
    """
    unittest_pattern: str = request.config.getini("unit_test_pattern")  # pyright:ignore
    return bool(re.search(unittest_pattern, str(request.path)))


@pytest.fixture(name="raw_books")
def fx_raw_books() -> list[Book | dict[str, Any]]:
    """Unstructured user representations."""

    return [
        {"book_name": "Text Book", "published_dt": "2022-01-01"},
    ]


@pytest.fixture(name="raw_words")
def fx_raw_words() -> list[Word | dict[str, Any]]:
    return [
        {
            "word_string": "have to",
            "word_lemma": "have to",
            "word_pos": "v",
            "is_multiple_words": True,
            "word_status": 1,
            "word_pronunciation": None,
            "word_explanation": "must do something",
            "word_counts": 2,
            "word_tokens": ["have", "to"],
        },
        {
            "word_string": "hello",
            "word_lemma": "hello",
            "word_pos": "NOUN",
            "is_multiple_words": False,
            "word_status": 1,
            "word_pronunciation": None,
            "word_explanation": "greeting",
            "word_counts": None,
            "word_tokens": ["hello"],
        },
    ]


@pytest.fixture()
def _patch_sqlalchemy_plugin(is_unit_test: bool, monkeypatch: MonkeyPatch) -> None:
    if is_unit_test:
        from app.lib import db

        monkeypatch.setattr(
            db.config.SQLAlchemyConfig,  # type:ignore[attr-defined]
            "on_shutdown",
            MagicMock(),
        )


@pytest.fixture(name="cap_logger")
def fx_cap_logger(monkeypatch: MonkeyPatch) -> CapturingLogger:
    """Used to monkeypatch the app logger, so we can inspect output."""
    import app.lib

    app.lib.log.configure(
        app.lib.log.default_processors,  # type:ignore[arg-type]
    )
    # clear context for every test
    clear_contextvars()
    # pylint: disable=protected-access
    logger = app.lib.log.controller.LOGGER.bind()
    logger._logger = CapturingLogger()
    # drop rendering processor to get a dict, not bytes
    # noinspection PyProtectedMember
    logger._processors = app.lib.log.default_processors[:-1]
    monkeypatch.setattr(app.lib.log.controller, "LOGGER", logger)
    monkeypatch.setattr(app.lib.log.worker, "LOGGER", logger)
    return logger._logger
