    
from datetime import date

from sqlalchemy import func, select, and_
from sqlalchemy.orm import aliased

from app.bookings.model import Bookings, Bookings
   
from app.database import async_session_maker  
from app.hotels.model import Hotels
from app.hotels.rooms.model import Rooms


class HotelDAO():  # может отличатся от видео 
    @classmethod    # 1) Получение списка отелей. 
    async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            b = aliased(Bookings)
            r = aliased(Rooms)
            h = aliased(Hotels)
            
            booking_for_dates = (select(b).filter
                                 (and_(
                                     b.date_from <= date_to,
                                     b.date_to >= date_from)
                                 )).cte("booking_for_dates")
            
            room_bookings = (select(r.hotel_id, func.count().label("booked_rooms"))
                             .select_from(r)
                             .join(booking_for_dates, r.id==booking_for_dates.c.room_id)
                             .group_by(r.hotel_id)).cte("room bookings")
            
            querry = (select(
                h.id,
                h.name,
                h.location,
                h.services,
                h.rooms_quantity, 
                h.image_id,
                (h.rooms_quantity - func.coalesce(room_bookings.c.booked_rooms, 0)).label("rooms_left")) # func.coalesce - функция SQL COALESCE(func.coalesce в алхимии) используется для обработки значений NULL в запросе к базе данных, возвращая первое не-NULL значение из списка выражений или значений столбцов . Она позволяет указать значение по умолчанию или резервное значение, если в данных встречаются значения NULL.
                .select_from(h)
                .join(room_bookings, h.id ==room_bookings.c.hotel_id, isouter=True)
                .filter(
                    h.location.contains(location),
                    (h.rooms_quantity - func.coalesce(room_bookings.c.booked_rooms, 0)) > 0              
            ))
            res = await session.execute(querry)
            return res.mappings().all()
        
    @classmethod #2) Получение списка комнат
    async def get_rooms_by_hotel(cls,
                                 hotel_id: str,
                                 date_from: date,
                                 date_to: date):
        async with async_session_maker() as session:
            r = aliased(Rooms)
            b = aliased(Bookings)
            h = aliased(Hotels)
            
            #relbook  - relevant bookings
            relbook = (select(
                r.id,
                func.count().label("booked_rooms"))
                       .select_from(r)
                       .join(b, r.id==b.room_id)
                       .filter(
                           b.date_from <= date_to,
                           b.date_to >= date_from
                       )
                       .group_by(r.id)
                        ).cte("rb")
            #relhot - relevant hotels
            relhot = (select(h)
                      .select_from(h)
                      .filter(h.id == hotel_id)
                      ).cte("rh")
            #Посмотреть компиляцию sql-запроса
            print("RB SQL")
            print(relbook.compile(compile_kwargs={"literal_binds": True}))
            
            querry = (select(
                relhot.c.id.label("hotel_id"),
                r.id,
                r.name,
                r.description,
                r.services,
                r.price,
                r.quantity,
                r.image_id,
                ((date_to - date_from).days * r.price).label("total_cost"),
                (r.quantity - func.coalesce(relbook.c.booked_rooms, 0)).label("rooms_left")) #В SQLAlchemy, func.coalesce() — это функция, которая используется для обработки значений NULL в запросах SQL. Она аналогична SQL-функции COALESCE, которая принимает один или несколько аргументов и возвращает первый ненулевой аргумент.
            .select_from(relhot)
            .join(r, relhot.c.id == r.hotel_id)
            .join(relbook, r.id == relbook.c.id, isouter=True)          
            )   
            
            res = await session.execute(querry)  
            return res.mappings().all()     
        
        

            