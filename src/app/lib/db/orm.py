"""Application ORM configuration."""

from __future__ import annotations

import json
from typing import Any

from advanced_alchemy.base import AuditColumns, orm_registry
from advanced_alchemy.base import BigIntBase as DatabaseModel
from advanced_alchemy.base import UUIDAuditBase as TimestampedDatabaseModel
from advanced_alchemy.repository.typing import ModelT  # noqa: TCH002
from sqlalchemy import String, Text, TypeDecorator
from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    mapped_column,
)

__all__ = ["DatabaseModel", "TimestampedDatabaseModel", "orm_registry", "model_from_dict", "AuditColumns", "SlugKey"]


class JSONType(TypeDecorator):
    """Represents a JSON data type."""

    impl = Text

    def process_bind_param(self, value, dialect):
        """Convert Python object to a JSON string before storing."""
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """Convert JSON string to a Python object after reading from database."""
        if value is not None:
            value = json.loads(value)
        return value


@declarative_mixin
class SlugKey:
    """Slug unique Field Model Mixin."""

    __abstract__ = True
    slug: Mapped[str] = mapped_column(String(length=100), index=True, nullable=False, unique=True, sort_order=-9)


def model_from_dict(model: ModelT, **kwargs: Any) -> ModelT:
    """Return ORM Object from Dictionary."""
    data = {}
    for column in model.__table__.columns:
        column_val = kwargs.get(column.name, None)
        if column_val is not None:
            data[column.name] = column_val
    return model(**data)  # type: ignore
