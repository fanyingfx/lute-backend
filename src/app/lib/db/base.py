from advanced_alchemy import AlembicAsyncConfig
from advanced_alchemy import AsyncSessionConfig
from litestar import Litestar

from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from litestar.contrib.sqlalchemy.base import BigIntBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
import ipdb

from app.lib import serialization
from app.lib import settings

engine = create_async_engine(
    settings.db.URL,
    future=True,
    json_serializer=serialization.to_json,
    json_deserializer=serialization.from_json,
)
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)
# async def init_db(app: Litestar) -> None:
#     async with app.state.db_engine.begin() as conn:
#         await conn.run_sync(BigIntBase.metadata.drop_all)
#         await conn.run_sync(BigIntBase.metadata.create_all)
# config = SQLAlchemyAsyncConfig(connection_string="sqlite+aiosqlite:///todo_async.sqlite")
# plugin = SQLAlchemyInitPlugin(config=config)
session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:////home/fan/PycharmProjects/lute-backend/data/test.db", session_config=session_config

    , alembic_config=AlembicAsyncConfig(
        version_table_name=settings.db.MIGRATION_DDL_VERSION_TABLE,
        script_config=settings.db.MIGRATION_CONFIG,
        script_location=settings.db.MIGRATION_PATH,
    ),
)  # Create 'db_session' dependency.
plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
