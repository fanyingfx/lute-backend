from __future__ import annotations

from typing import Any

import anyio
import click
from pydantic import EmailStr
from rich import get_console

from app.domain.books.dtos import BookCreate
from app.domain.books.services import BookService
from app.lib import log

__all__ = [
]


console = get_console()
"""Pre-configured CLI Console."""

logger = log.get_logger()




