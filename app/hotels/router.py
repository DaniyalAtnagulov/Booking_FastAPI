import asyncio
from datetime import date, datetime

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),         
) -> list[SHotelInfo]:
    #  Проверка 1: Дата заезда >= Дата выезда
    if date_from >= date_to:
        raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда!")

    #  Проверка 2: Дата выезда - Дата заезда > 30 дней
    max_stay = 30
    if (date_to - date_from).days > max_stay:
        raise HTTPException(status_code=400, detail=f"Максимальный срок проживания — {max_stay} дней!")

    #  Эмуляция задержки
    await asyncio.sleep(3)

    # Получение данных
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)
    return hotels
