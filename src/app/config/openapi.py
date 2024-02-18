# mypy: ignore-errors
"""OpenAPI Config."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Contact

__all__ = ["config"]

from app.lib import settings

load_dotenv()

config = OpenAPIConfig(
    title=os.getenv("OPENAPI_TITLE", default=settings.openapi.TITLE),
    description=os.getenv(
        "OPENAPI_DESCRIPTION",
        "Litestar template for Railway",
    ),
    servers="http://localhost:8000" if os.getenv("DEBUG", "false").lower() == "true" else "/",  # type: ignore[arg-type]
    external_docs=os.getenv(  # type: ignore[arg-type]
        "OPENAPI_EXTERNAL_DOCS", "https://github.com/JacobCoffee/litestar-template/docs/"  # type: ignore[arg-type]
    ),
    version=settings.openapi.VERSION,
    contact=Contact(
        name=os.getenv("OPENAPI_CONTACT_NAME", "Administrator"),
        email=os.getenv("OPENAPI_CONTACT_EMAIL", "admin@localhost"),
    ),
    use_handler_docstrings=True,
    root_schema_site="elements",
    path=os.getenv("OPENAPI_PATH", "/api"),
)
"""OpenAPI config for app."""
