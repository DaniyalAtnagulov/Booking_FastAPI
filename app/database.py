from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
#from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker​​​​​​

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):  # Класс Base аккумулирует данные о всех моделях, которые наследованы от него В комментах уточнили что Класс Base не аккумулуриует данные о всех моделях, от него наследованных, а просто его метадата сохраняет ссылки на дочерние классы
    pass


