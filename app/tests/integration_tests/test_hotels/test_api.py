import pytest

@pytest.mark.parametrize(
    "date_from, date_to, expected_status, expected_detail",
    [
        ("2030-05-10", "2030-05-05", 400, "Дата заезда должна быть раньше даты выезда!"),
        ("2030-05-01", "2030-06-10", 400, "Максимальный срок проживания — 30 дней!"),
        ("2030-05-01", "2030-05-15", 200, None),  # Валидные даты
    ]
) 
@pytest.mark.asyncio
async def test_get_hotels_by_location(authenticated_ac, date_from, date_to, expected_status, expected_detail):
    response = await authenticated_ac.get(f"/hotels/Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20?date_from={date_from}&date_to={date_to}")
    assert response.status_code == expected_status
    if expected_status == 400:
        assert response.json()["detail"] == expected_detail
        
""" pytest -v -s app/tests/integration_tests/test_hotels/test_api.py """