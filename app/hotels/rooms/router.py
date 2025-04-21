from datetime import date

from app.hotels.dao import HotelDAO
from app.hotels.rooms.schemas import SAvaibleRoom
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date)-> list[SAvaibleRoom]:
    
    res = HotelDAO.get_rooms_by_hotel(hotel_id, date_from, date_to)
    return res






# Можно еще реализовать Получение конкретного отеля (опционально, может пригодиться для фронтенда)

# Пример эндпоинта: /hotels/id/1.
# HTTP метод: GET.
# HTTP код ответа: 200.
# Описание: возвращает все данные по одному отелю.
# Нужно быть авторизованным: нет.
# Параметры: параметр пути hotel_id.
# Ответ пользователю: для отеля должно быть указано: id, name, location, services, rooms_quantity, image_id.
    
    