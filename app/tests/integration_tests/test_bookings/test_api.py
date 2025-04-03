from httpx import AsyncClient
import pytest



@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    *[(4,"2030-05-01", "2030-05-15", 200)]*8,
    (4,"2030-05-01", "2030-05-15", 200),
    (4,"2030-05-01", "2030-05-15", 200),
])
async def test_add_and_get_booking(room_id,date_from,date_to,status_code,authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
         "date_from": date_from,
         "date_to": date_to   
    })
    
    assert response.status_code==status_code 
    
    
    """pytest -v -s app/tests/integration_tests/test_bookings/test_api.py"""