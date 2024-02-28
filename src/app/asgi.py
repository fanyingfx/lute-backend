# pylint: disable=[invalid-name,import-outside-toplevel]
# SPDX-FileCopyrightText: 2023-present Cody Fincher <cody.fincher@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


def create_app() -> Litestar:
    """Create ASGI application."""

    from litestar import Litestar

    # from uuid_utils import UUID
    from app.config import app as config
    from app.config.base import get_settings
    from app.domain.word.services import on_word_updated

    # from app.lib import db
    # from app.domain.accounts import signals as account_signals
    # from app.domain.accounts.dependencies import provide_user
    # from app.domain.accounts.guards import auth
    # from app.domain.teams import signals as team_signals
    # from app.lib.dependencies import create_collection_dependencies
    from app.server import openapi, plugins, routers, static_files, template

    # dependencies = {constants.USER_DEPENDENCY_KEY: Provide(provide_user)}
    # dependencies.update(create_collection_dependencies())
    settings = get_settings()

    return Litestar(
        cors_config=config.cors,
        # dependencies=dependencies,
        debug=settings.app.DEBUG,
        openapi_config=openapi.config,
        route_handlers=routers.route_handlers,
        static_files_config=static_files.config,
        plugins=[
            plugins.app_config,
            plugins.structlog,
            plugins.alchemy,
            # db.plugin,
            # plugins.vite,
            # plugins.saq,
            # plugins.granian,
        ],
        template_config=template.config,
        # signature_namespace={"UUID": UUID},
        # on_app_init=[auth.on_app_init],
        # listeners=[account_signals.user_created_event_handler, team_signals.team_created_event_handler],
        listeners=[on_word_updated],
    )


app = create_app()
