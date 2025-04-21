import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_booking_lifecycle(authenticated_ac: AsyncClient):
    # Шаг 1: Добавляем 3 бронирования
    booking_data = [
        {"room_id": 4, "date_from": "2030-06-01", "date_to": "2030-06-05"},
        {"room_id": 4, "date_from": "2030-06-06", "date_to": "2030-06-10"},
        {"room_id": 4, "date_from": "2030-06-11", "date_to": "2030-06-15"},
    ]

    for data in booking_data:
        response = await authenticated_ac.post("/bookings/add", json=data)
        assert response.status_code == 200

    # Шаг 2: Получаем все бронирования
    response = await authenticated_ac.get("/bookings/get")
    assert response.status_code == 200
    bookings = response.json()
    assert len(bookings) == len(booking_data)

    # Шаг 3: Удаляем все бронирования
    for booking in bookings:
        booking_id = booking["id"]
        delete_response = await authenticated_ac.delete(f"/bookings/{booking_id}")
        assert delete_response.status_code == 204

    # Шаг 4: Проверяем, что бронирований больше нет
    response = await authenticated_ac.get("/bookings/get")
    assert response.status_code == 200
    assert response.json() == []

    # Шаг 5: Повторно создаём одну бронь
    response = await authenticated_ac.post(
        "/bookings/add",
        json={
            "room_id": 4,
            "date_from": "2030-06-20",
            "date_to": "2030-06-25",
        },
    )
    assert response.status_code == 200
    
    
    """pytest --envfile .env.test tests/integration_tests/test_bookings/test_api.py -s -v"""