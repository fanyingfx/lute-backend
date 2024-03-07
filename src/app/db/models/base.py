import json
from collections.abc import Hashable
from typing import Any, Self, cast

from advanced_alchemy.base import orm_registry
from advanced_alchemy.repository.typing import ModelT
from sqlalchemy import (
    ColumnElement,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_mixin, mapped_column
from sqlalchemy.types import String, Text, TypeDecorator

# if TYPE_CHECKING:


@declarative_mixin
class SlugKey:
    """Slug unique Field Model Mixin."""

    __abstract__ = True
    slug: Mapped[str] = mapped_column(String(length=100), nullable=False, unique=True, sort_order=-9)


def model_from_dict(model: ModelT, **kwargs: Any) -> ModelT:
    """Return ORM Object from Dictionary."""
    data = {column.name: kwargs.get(column.name) for column in model.__table__.columns if column.name in kwargs}
    return model(**data)  # type: ignore


class SQLQuery(DeclarativeBase):
    """Base for all SQLAlchemy custom mapped objects."""

    __allow_unmapped__ = True
    registry = orm_registry

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """Convert model to dictionary.

        Returns:
            dict[str, Any]: A dict representation of the model
        """
        exclude = exclude.union("_sentinel") if exclude else {"_sentinel"}
        return {field.name: getattr(self, field.name) for field in self.__table__.columns if field.name not in exclude}


class UniqueMixin:
    @classmethod
    async def as_unique(
        cls,
        session: AsyncSession | async_scoped_session[AsyncSession],
        *args: Any,
        **kwargs: Any,
    ) -> Self:
        key = cls, cls.unique_hash(*args, **kwargs)
        cache = getattr(session, "_unique_cache", None)
        if cache is None:
            cache = {}
            session._unique_cache = cache  # type: ignore
        if obj := cache.get(key):
            return cast("Self", obj)

        with session.no_autoflush:
            statement = select(cls).where(cls.unique_filter(*args, **kwargs)).limit(1)
            if (obj := (await session.scalars(statement)).first()) is None:
                session.add(obj := cls(*args, **kwargs))
        cache[key] = obj
        return obj

    @classmethod
    def unique_hash(cls, *arg: Any, **kw: Any) -> Hashable:
        msg = "Implement this in subclass"
        raise NotImplementedError(msg)

    @classmethod
    def unique_filter(cls, *arg: Any, **kw: Any) -> ColumnElement[bool]:
        msg = "Implement this in subclass"
        raise NotImplementedError(msg)


class JSONType(TypeDecorator):
    """Represents a JSON data type."""

    impl = Text

    def process_bind_param(self, value, dialect):  # type: ignore
        """Convert Python object to a JSON string before storing."""
        if value is not None:
            value = json.dumps(value, ensure_ascii=False)
        return value

    def process_result_value(self, value, dialect):  # type: ignore
        """Convert JSON string to a Python object after reading from database."""
        if value is not None:
            value = json.loads(value)
        return value

    # https://stackoverflow.com/questions/15668115/alembic-how-to-migrate-custom-type-in-a-model/43810638#43810638
    def __repr__(self):  # type: ignore
        return f"{self.impl!r}"


# from advanced_alchemy import AlembicAsyncConfig, AsyncSessionConfig
# from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
# from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
#
# from app.lib import serialization, settings
#
# engine = create_async_engine(
#     settings.db.URL,
#     future=True,
#     json_serializer=serialization.to_json,
#     json_deserializer=serialization.from_json,
# )
#
# async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)
#
# session_config = AsyncSessionConfig(expire_on_commit=False)
# db_config = SQLAlchemyAsyncConfig(
#     connection_string="sqlite+aiosqlite:///todo.sqlite",
#     create_all=True,
# )
