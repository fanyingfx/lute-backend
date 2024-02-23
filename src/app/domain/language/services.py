from typing import Any

from app.domain.language.models import Language
from app.lib.repository import SQLAlchemyAsyncRepository
from app.lib.service import SQLAlchemyAsyncRepositoryService


class LanguageRepository(SQLAlchemyAsyncRepository[Language]):
    """Word SQLAlchemy Repository."""

    model_type = Language


class LanguageService(SQLAlchemyAsyncRepositoryService[Language]):
    """Handles database operations for users."""

    repository_type = LanguageRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: LanguageRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
