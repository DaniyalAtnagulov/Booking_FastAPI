from datetime import date
from typing import Union
from fastapi import APIRouter, Depends, Request
from pydantic import TypeAdapter, parse_obj_as
from sqlalchemy import select
from app.bookings.dao import BookingDAO
from app.database import async_session_maker
from app.bookings.model import Bookings
from app.bookings.schemas import SBooking, SBookingWithRoomInfo
from app.exceptions import BookingNotExist, RoomCannotBeBooked
from app.hotels.dao import HotelDAO
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.model import Users
from fastapi import BackgroundTasks

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings(user:Users=Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)
    #print(user, type(user), user.email)


@router.post("")             #стоит переделать, как в 2.1              
async def add_bookings(
    room_id: int, date_from: date, date_to: date,
    user: Users=Depends(get_current_user),
    #background_tasks: BackgroundTasks
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SBooking).validate_python(booking).model_dump()     #Возможно стоит использовать иную схему SBooking
    # вариант через celery
    send_booking_confirmation_email.delay(booking, user.email)
    # вариант через встроенный background tasks(в tasks.py не забыть закомментировать @celery.task)
    #backgroundtasks.add_task(send_booking_confirmation_email, booking, user.email) 
    return booking
    
@router.delete("/{booking_id}") # Удаление
async def cancel_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),  
) -> dict[str, str]:
    success = await BookingDAO.delete(booking_id, user.id)

    if not success:
        raise BookingNotExist

    return {"message": "Бронь отменена"}


@router.get("")
async def get_by_user_id(user_id: int)-> list[SBookingWithRoomInfo]:
    return await BookingDAO.find_by_user
   
# @router.get("")
# async def get_bookings(request: Request):
#     return await BookingDAO.find_all()

#-> list[dict[str, SBooking]]: # !ремарка устарела! замороченная запись после стрелки(->) т.к. использовал result.mappings().all() альтернативой является results.scalars().all() но тогда придется использовать класс class Config() в schemas.py
    #return await BookingDAO.find_all()        # @router.get("")
                                                # async def get_bookings():
                                                #     return await BookingRepository.find_all(Booking.id > 1, Booking.user_id == 2)
 
# 
# @router.get("/id")                                  для других методов класса
# async def get_booking_one() -> Union[SBooking,None]:    
#     #return await BookingDAO.find_by_id(1)
#     return await BookingDAO.find_one_or_none(room_id=1)



#response_model = None отключает валидацию, что в корне неверно если хотите использовать mappings(), вот пример кода:
 # Ключом может быть любая строка
# @router.get("")
# async def get_bookings() -> list[dict[str, SBooking]]:
#     return await BookingDAO.find_all()

# # Если нужен определенный ключ

# from typing import Literal

# BookingsList = list[dict[Literal["Booking"], SBooking]]




    
    



