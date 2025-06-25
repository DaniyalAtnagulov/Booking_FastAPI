import asyncio
import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# Добавляем путь к корню проекта для импортов
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from app.config import settings
from app.database import Base
from app.users.model import Users  # импорт моделей нужен для Alembic autogenerate
from app.bookings.model import Bookings
from app.hotels.model import Hotels
from app.hotels.rooms.model import Rooms

# Конфиг Alembic
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Устанавливаем URL для миграций:
# Offline — синхронный URL
# Online — асинхронный URL

def run_migrations_offline():
    """Запуск миграций в offline режиме (использует sync URL)"""
    url = settings.DATABASE_SYNC_URL
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


async def run_migrations_online():
    """Запуск миграций в online режиме (асинхронно)"""
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

