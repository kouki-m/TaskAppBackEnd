import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import async_engine_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import app.models.tasks
from app.db import database

# .envファイルを読み込み
load_dotenv()

target_metadata = database.Base.metadata
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # alembic.iniに渡すDBの環境変数
    config.set_section_option("alembic", "DB_USER", os.environ.get("MYSQL_USER"))
    config.set_section_option("alembic", "DB_NAME", os.environ.get("MYSQL_DB_NAME"))
    config.set_section_option(
        "alembic", "DB_PASSWORD", os.environ.get("MYSQL_ROOT_PASSWORD")
    )
    config.set_section_option("alembic", "DB_HOST", os.environ.get("MYSQL_HOST"))

    print(
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_DB_NAME"),
        os.environ.get("MYSQL_ROOT_PASSWORD"),
    )

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
