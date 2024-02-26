from litestar.openapi.config import OpenAPIConfig

from app.__about__ import __version__ as current_version
from app.config import get_settings

settings = get_settings()

config = OpenAPIConfig(
    title=settings.app.NAME,
    version=current_version,
    use_handler_docstrings=True,
    root_schema_site="swagger",
)
"""OpenAPI config for app.  See OpenAPISettings for configuration."""
