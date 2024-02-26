"""Application Modules."""
from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.language.controllers import LanguageController
from app.domain.word.controllers import WordController
from app.domain.book.controllers import BookController
from app.domain.system.controllers import SystemController
from app.domain.web.controllers import WebController

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler


route_handlers: list[ControllerRouterHandler] = [
    # AccessController,
    # UserController,
    # TeamController,
    # UserRoleController,
    # #  TeamInvitationController,
    # TeamMemberController,
    # TagController,
    SystemController,
    WebController,
    LanguageController,
    WordController,
    BookController
]
