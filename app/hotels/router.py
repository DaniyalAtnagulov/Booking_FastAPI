import asyncio
from datetime import date, datetime
from fastapi import APIRouter, Query
from app.hotels.dao import HotelDAO 
from app.hotels.schemas import SHotelInfo

from fastapi_cache.decorator import cache

router = APIRouter(prefix="/Hotels", tags=["Отели"])

@router.get("/{location}") #отличатся от видео 
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например,{datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например,{datetime.now().date()}"),         
) -> list[SHotelInfo]:
    await asyncio.sleep(3)
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)                   #отличатся от видео
    return hotels