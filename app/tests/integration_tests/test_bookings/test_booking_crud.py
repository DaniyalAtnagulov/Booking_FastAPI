import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_booking_crud_operations(authenticated_ac: AsyncClient):
    # Шаг 1: Добавление брони
    create_payload = {
        "room_id": 4,
        "date_from": "2030-07-01",
        "date_to": "2030-07-05"
    }
    create_response = await authenticated_ac.post("/bookings/add", json=create_payload)
    assert create_response.status_code == 200

    booking_data = create_response.json()
    booking_id = booking_data.get("id")
    assert booking_id is not None, "ID не получен после создания бронирования"

    # Шаг 2: Получение конкретной брони по ID
    get_response = await authenticated_ac.get(f"/bookings/{booking_id}")
    assert get_response.status_code == 200
    booking = get_response.json()
    assert booking["room_id"] == create_payload["room_id"]
    assert booking["date_from"] == create_payload["date_from"]
    assert booking["date_to"] == create_payload["date_to"]

    # Шаг 3: Удаление брони
    delete_response = await authenticated_ac.delete(f"/bookings/{booking_id}")
    assert delete_response.status_code == 204

    # Шаг 4: Попытка получить удалённую бронь
    get_after_delete = await authenticated_ac.get(f"/bookings/{booking_id}")
    assert get_after_delete.status_code == 404  # Ожидаем, что бронь больше не найдена
    
    
    
    """pytest --envfile .env.test tests/integration_tests/test_bookings/test_booking_crud.py -s -v"""