from __future__ import annotations

import re
from datetime import date
from typing import TYPE_CHECKING, Any

import pytest

from app.config import base
from app.db.models import Book, Language, Word

if TYPE_CHECKING:
    from litestar import Litestar
    from pytest import FixtureRequest, MonkeyPatch

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
def _patch_settings(monkeypatch: MonkeyPatch) -> None:
    """Path the settings."""

    settings = base.Settings.from_env(".env.testing")

    def get_settings(dotenv_filename: str = ".env.testing") -> base.Settings:
        return settings

    monkeypatch.setattr(base, "get_settings", get_settings)


# @pytest.fixture(scope="session")
# def event_loop() -> abc.Iterator[asyncio.AbstractEventLoop]:
#     """Scoped Event loop.
#
#     Need the event loop scoped to the session so that we can use it to check
#     containers are ready in session scoped containers fixture.
#     """
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#     try:
#         yield loop
#     finally:
#         loop.close()


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


@pytest.fixture(name="test_app")
def fx_app(pytestconfig: pytest.Config, monkeypatch: MonkeyPatch) -> Litestar:
    """App fixture.

    Returns:
        An application instance, configured via plugin.
    """
    from app.asgi import app

    return app


@pytest.fixture(name="is_unit_test")
def fx_is_unit_test(request: FixtureRequest) -> bool:
    """Uses the ini option `unit_test_pattern` to determine if the test is part
    of unit or integration tests.
    """
    unittest_pattern: str = request.config.getini("unit_test_pattern")  # pyright:ignore
    return bool(re.search(unittest_pattern, str(request.path)))


@pytest.fixture(name="raw_languages")
def fx_raw_language() -> list[Language | dict[str, Any]]:
    return [
        {"language_name": "English", "parser_name": "english", "RTL": False},
    ]


@pytest.fixture(name="raw_books")
def fx_raw_books() -> list[Book | dict[str, Any]]:
    """Unstructured user representations."""

    return [
        {"book_name": "Text Book", "language_id": 1, "published_at": date(2022, 1, 1)},
    ]


@pytest.fixture(name="raw_words")
def fx_raw_words() -> list[Word | dict[str, Any]]:
    return [
        {
            "language_id": 1,
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
            "language_id": 1,
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


# @pytest.fixture()
# def _patch_worker(
#     is_unit_test: bool,
#     monkeypatch: MonkeyPatch,
#     event_loop: Iterator[asyncio.AbstractEventLoop],
# ) -> None:
#     """We don't want the worker to start for unit tests."""
#     if is_unit_test:
#         from litestar_saq import base
#
#         monkeypatch.setattr(base.Worker, "on_app_startup", MagicMock())
#         monkeypatch.setattr(base.Worker, "stop", MagicMock())
