from app.database import async_session_maker

from sqlalchemy import RowMapping, insert, select

class BaseDAO:
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            querry = select(cls.model).filter_by(id=model_id)
            result = await session.execute(querry)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by) -> RowMapping | None:  # noqa: ANN003
        """Возвращает полную строку или None.
        cls.model.__table__.columns  =>   {'id': 1, ...}
        cls.model                    =>   {'Candies': <db.candies_model.Candies>}"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return  result.mappings().one_or_none()
    
    @classmethod
    async def find_all(cls,**filter_by):
        async with async_session_maker() as session:
            querry = select(cls.model).filter_by(**filter_by)
            result = await session.execute(querry)
            return result.mappings().all()     #result.sacalars().all() нельзя дважды вызвать, для этого нужно создать отдельную переменную, касательно result.mappings().all() - еще нужно будет проверить    
                                               # results.all() -> list[tuple(model)]
                                                # results.scalars().all() -> list[model]
                                                 # results.mappings().all() -> list[dict(model)] 
                                                 #   последняя предпочтительна она сразу же возвращает список словариков в виде {столбец1: значение, столбец2: значение}.раздел 1.6 Шаг 5 
    
    
    
    
#Выше приведена реализация через метод filter_by, но что, если мы захотим отфильтровать данные, например, где id > 5? Данный метод не позволит нам этого сделать по причине того, что в него мы передаем словарь key-value, и не можем явно прописать условия фильтрация для знаков больше, меньше и т.д.

# Существует метод filter, который принимает не **kwargs, а *args, и в него можно передать такого типа условия.

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit() # фиксирует изменния в базе данных(update, delete, insert) commit() всегшда требуется , когда обновляем данные












# @classmethod
# async def find_all(cls, *filter_by):
#     async with async_session_maker() as session:
#         query = select(cls.model.__table__.columns).filter(*filter_by)
#         result = await session.execute(query)
#         return result.mappings().all()

# Изменение запроса в эндпоинте:

# @router.get("")
# async def get_bookings():
#     return await BookingRepository.find_all(Booking.id > 1, Booking.user_id == 2)
   