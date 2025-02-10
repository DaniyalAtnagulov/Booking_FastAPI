from datetime import date, datetime
from fastapi import APIRouter, Query
from app.hotels.dao import HotelDAO 
from app.hotels.schemas import SHotelInfo

router = APIRouter(prefix="/Hotels", tags=["Отели"])

@router.get("") #отличатся от видео 
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например,{datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например,{datetime.now().date()}"),         
) -> list[SHotelInfo]:
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)                   #отличатся от видео
    return hotels