"""Static files configuration."""

from __future__ import annotations

from pathlib import Path

from litestar.static_files.config import StaticFilesConfig

config = [
    StaticFilesConfig(
        directories=[Path(__file__).parent.parent / "static"],
        path="static",
        name="static",
        html_mode=True,
        opt={"exclude_from_auth": True},
    ),
    StaticFilesConfig(
        directories=[Path(__file__).parent.parent / "static" / "web"],
        path="web",
        name="web",
        html_mode=True,
        opt={"exclude_from_auth": True},
    ),
    StaticFilesConfig(
        directories=[Path(__file__).parent.parent / "static" / "web" / "assets"],
        path="assets",
        name="assets",
        html_mode=True,
        opt={"exclude_from_auth": True},
    ),
]
