from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
#from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker​​​​​​

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.DATABASE_TEST_URL
    DATABASE_PARAMS = {"poolclass": NullPool} #В тестовом режиме (TEST) используется NullPool, чтобы каждый запрос создавал новое соединение с базой.В обычном режиме (prod/dev) соединения управляются стандартным пулом (по умолчанию QueuePool), что повышает производительность.
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):  # Класс Base аккумулирует данные о всех моделях, которые наследованы от него В комментах уточнили что Класс Base не аккумулуриует данные о всех моделях, от него наследованных, а просто его метадата сохраняет ссылки на дочерние классы
    pass


# Оптимизация Можно сделать метод, который будет принимать параметры и избежать дублирования кода:


# def _build_db_url(self, user, password, host, port, name):
#     return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

# @property
# def DATABASE_URL(self):
#     return self._build_db_url(self.DB_USER, self.DB_PASS, self.DB_HOST, self.DB_PORT, self.DB_NAME)

# @property
# def DATABASE_TEST_URL(self):
#     return self._build_db_url(self.TEST_DB_USER, self.TEST_DB_PASS, self.TEST_DB_HOST, self.TEST_DB_PORT, self.TEST_DB_NAME)