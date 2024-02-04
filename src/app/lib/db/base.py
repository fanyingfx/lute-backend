from advanced_alchemy import AlembicAsyncConfig, AsyncSessionConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.lib import serialization, settings

engine = create_async_engine(
    settings.db.URL,
    future=True,
    json_serializer=serialization.to_json,
    json_deserializer=serialization.from_json,
)
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)
# async def init_db(app: Litestar) -> None:
#     async with app.state.db_engine.begin() as conn:
session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:////home/fan/PycharmProjects/lute-backend/data/test.db",
    session_config=session_config,
    alembic_config=AlembicAsyncConfig(
        version_table_name=settings.db.MIGRATION_DDL_VERSION_TABLE,
        script_config=settings.db.MIGRATION_CONFIG,
        script_location=settings.db.MIGRATION_PATH,
    ),
)  # Create 'db_session' dependency.
plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
