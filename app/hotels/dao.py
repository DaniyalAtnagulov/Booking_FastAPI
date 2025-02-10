    
from datetime import date

from sqlalchemy import func, select, and_, aliased
from sqlalchemy.orm import aliased

from app.bookings.model import Bookings, Bookingss
   
from database import async_session_maker  
from app.hotels.model import Hotels, Rooms


class HotelDAO():  # может отличатся от видео 
    @classmethod
    async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker as session:
            b = aliased(Bookings)
            r = aliased(Rooms)
            h = aliased(Hotels)
            
            booking_for_dates = (select(b).filter
                                 (and_(
                                     b.date_from <= date_to,
                                     b.date_to >= date_from)
                                 )).cte("booking_for_dates")
            
            room_bookings = ()