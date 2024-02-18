from __future__ import annotations

from rich import get_console

from app.lib import log

__all__ = ['console','logger']


console = get_console()
"""Pre-configured CLI Console."""

logger = log.get_logger()
