"""Litestar template application."""

from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("create_app",)


if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler


def create_app():
    from advanced_alchemy import RepositoryError
    from dotenv import load_dotenv
    from litestar import Litestar
    from litestar.config.cors import CORSConfig

    from app.config import openapi, static_files, template
    from app.domain import books
    from app.domain.home.controllers import HomeController
    from app.lib import db, exceptions, log, repository

    load_dotenv()
    book_controllers = [books.controllers.BookController, books.controllers.BookTextController]
    routes: list[ControllerRouterHandler] = [HomeController, *book_controllers]
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
        plugins=[db.plugin],
        # --- Lifecycle
        cors_config=cors_config,
        on_startup=[lambda: log.configure(log.default_processors)],
        on_app_init=[repository.on_app_init],
        debug=True,
        pdb_on_exception=True,
    )
