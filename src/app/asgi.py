"""Litestar template application."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar
def create_app():
    from advanced_alchemy import RepositoryError
    from dotenv import load_dotenv
    from litestar import  Litestar
    from litestar.config.cors import CORSConfig
    from litestar.types import ControllerRouterHandler

    from app.config import openapi, static_files, template
    from app.domain import books
    from app.lib import db,exceptions,log
    from app.lib import repository
    from app.domain.books.controllers.book import BookController
    from app.domain.home.controllers import home



    load_dotenv()
    routes: list[ControllerRouterHandler] = [ home,books.controllers.BookController]
    """List of routes."""
    cors_config = CORSConfig(allow_origins=["*"])


    return Litestar(
        route_handlers=[*routes],
        # --- Config
        template_config=template.config,
        openapi_config=openapi.config,
        static_files_config=static_files.config,
        exception_handlers={
            exceptions.ApplicationError: exceptions.exception_to_http_response,
            RepositoryError: exceptions.exception_to_http_response,
        },
        before_send=[log.controller.BeforeSendHandler()],
        middleware=[log.controller.StructlogLoggingMiddleware],
        logging_config=log.config,
        # static_files_config=static_files.config,
        plugins=[db.plugin],
        # --- Lifecycle
        cors_config=cors_config,
        # on_startup=[],
        on_startup=[ lambda: log.configure(log.default_processors)],
        on_app_init=[repository.on_app_init],
        # pdb_on_exception=True,
        debug=True,


    )
