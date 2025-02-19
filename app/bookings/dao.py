'''dao - data access object Данный файл можно назвать и service.py, и repo.py(репозиторий) суть в будет в том, чтобы он отделял работу с БД
Представляет собой Паттерн для абстракции, содержащий в себе всё, что относится к способу хранения данных. Он предназначен для разделения бизнес-логики от деталей реализации слоя доступа к данным. 
Его рекомендуется использовать в любых средних и больших проектах.
В русскоязычном коммьюнити я чаще встречаюсь с названием Репозиторий, нежели DAO, хотя они оба отвечают за отделение слоя работы с базой данных от бизнес-логики.

По поводу именования, точно ли service.py будет эквивалентно dao.py? Посмотрела гитхаб с best practices по FastAPI,  там указано, что в service.py  принято хранить бизнес логику. Возможно что-то не так поняла)

 Да, действительно, в service.py/command.py обычно хранится логика приложения, а внутри dao.py/repository.py обращение к базе данных. В течение 2 недель дополню курс материалом про слои приложения и уведомлю всех учеников по почте
'''

from datetime import date
from app.bookings.model import Bookings
from app.dao.base import BaseDAO
from sqlalchemy import and_, delete, insert, or_, select, func
from sqlalchemy.orm import aliased

from app.database import async_session_maker, engine
from app.hotels.rooms.model import Rooms

class BookingDAO(BaseDAO):
    model = Bookings
    
    @classmethod
    async def add(
        cls,
        user_id: int, 
        room_id: int, 
        date_from: date, 
        date_to: date
        ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                            
                        )
                    )
                )
            ).cte("booked_rooms") 
            
            """
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id   
            """
            
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left") 
                ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id==room_id).group_by( # вроде и как правильно работает /только .where(Rooms.id==1) работает, хоть автор ролика и исправил на .where(Rooms.id==room_id)
                Rooms.quantity, booked_rooms.c.room_id
                )
            print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            
            rooms_left = await session.execute(get_rooms_left)
            rooms_left : int = rooms_left.scalar()
            #print(rooms_left.scalar())
            
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
                    
            else:
                return None
            
    @classmethod # УДАЛЕНИЕ
    async def delete(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            delete_booking = (
                delete(Bookings)
                .where(Bookings.id == booking_id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(delete_booking)
            await session.commit()
            return result.rowcount > 0

    @classmethod #3) Получение списка бронирований 
    async def find_by_user(cls, user_id):
        async with async_session_maker() as session:
            r = aliased(Rooms)
            b = aliased(Bookings)
            
            querry = (select(
                b.id,
                b.room_id,
                b.user_id,
                b.date_from,
                b.date_to,
                b.price,
                b.total_cost,
                b.total_days,
                r.image_id,
                r.name,
                r.description,
                r.services
            )
                      .filter(b.user_id == user_id)
                      .select_from(b)
                      .join(r, b.user_id ==r.id, isouter=True)
                      )
            result = await session.execute(querry)
            return result.mappings.all()
            