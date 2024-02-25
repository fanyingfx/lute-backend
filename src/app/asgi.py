"""Litestar template application."""

from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("create_app",)

from litestar import Litestar

from app.lib import settings

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler


def create_app(debug: bool = settings.app.DEBUG) -> Litestar:
    from advanced_alchemy import RepositoryError
    from dotenv import load_dotenv
    from litestar.config.cors import CORSConfig

    from app.config import openapi, static_files, template
    from app.domain import book, language, word
    from app.domain.home.controllers import HomeController
    from app.domain.word.services import on_word_updated
    from app.lib import db, exceptions, log, repository

    load_dotenv()
    book_controllers = [book.controllers.BookController, book.controllers.BookTextController]
    words_controllers = [word.controllers.WordController]
    language_controllers = [language.controllers.LanguageController]
    routes: list[ControllerRouterHandler] = [
        HomeController,
        *book_controllers,
        *words_controllers,
        *language_controllers,
    ]
    """List of routes."""
    cors_config = CORSConfig(allow_origins=["*"])

    return Litestar(
        route_handlers=[*routes],
        listeners=[on_word_updated],
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
        on_startup=[lambda: log.configure(log.default_processors)],  # type: ignore[arg-type]
        on_app_init=[repository.on_app_init],
        debug=debug,
    )
