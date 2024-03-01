"""Static files configuration."""

from __future__ import annotations

from pathlib import Path

from litestar.static_files import create_static_files_router

#
static_route_handlers = [
    create_static_files_router(
        directories=[Path(__file__).parent.parent / "static"],
        path="static",
        name="static",
    ),
    create_static_files_router(
        directories=[Path(__file__).parent.parent / "static" / "web"],
        path="web",
        name="web",
    ),
    create_static_files_router(
        directories=[Path(__file__).parent.parent / "static" / "web" / "assets"],
        path="assets",
        name="assets",
    ),
]
