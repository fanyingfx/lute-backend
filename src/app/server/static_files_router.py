"""Static files configuration."""

from __future__ import annotations

from pathlib import Path

from litestar.static_files import create_static_files_router

#
STATIC_PATH = Path(__file__).parent.parent / "static"
static_route_handlers = [
    create_static_files_router(
        directories=[STATIC_PATH, STATIC_PATH / "web", STATIC_PATH / "web" / "assets"],
        path="static",
        name="static",
        tags=["static"],
    ),
]
