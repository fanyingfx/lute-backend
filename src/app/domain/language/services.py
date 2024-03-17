from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import InstrumentedAttribute

import app.domain.parser.language_parsers.paser_config
from app.db.models.language import Language

# from app.domain.parser import parser_helper
from app.lib.exceptions import LanguageParserError
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService


class LanguageRepository(SQLAlchemyAsyncRepository[Language]):
    """Word SQLAlchemy Repository."""

    model_type = Language


class LanguageService(SQLAlchemyAsyncRepositoryService[Language]):
    """Handles database operations for users."""

    repository_type = LanguageRepository
    match_fields = ["name"]

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: LanguageRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def create(
        self,
        data: Language | dict[str, Any],
        auto_commit: bool | None = True,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> Language:
        db_obj = await self.to_model(data, "create")
        if not app.domain.parser.language_parsers.paser_config.parser_exists(db_obj.parser_name):
            raise LanguageParserError(f"Parser '{db_obj.parser_name}' is not found")
        return await super().create(data=db_obj, auto_commit=auto_commit)

    async def update(
        self,
        data: Language | dict[str, Any],
        item_id: Any | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> Language:
        return await super().update(item_id=item_id, data=data, auto_commit=True)

    async def to_model(self, data: Language | dict[str, Any], operation: str | None = None) -> Language:
        return await super().to_model(data, operation)
