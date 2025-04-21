import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", *[
    [(4, "2030-05-01", "2030-05-15", i, 201) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
    ])
async def test_add_and_get_vooking(room_id,date_from,date_to,status_code,booked_rooms,
                                   authenticated_ac:AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })
    
    assert response.status_code == status_code
    response = await authenticated_ac.get("/bookings")
    
    assert len(response.json()) == booked_rooms
    
    
    
# @pytest.mark.parametrize("email,password,status_code", [
#     ("kot@pes.com", "kotopes", 200),
#     ("kot@pes.com", "kot0pes", 409),
#     ("pes@kot.com", "pesokot", 200),
#     ("abcde", "pesokot", 422)
# ])
# async def test_resister_user(email, password, status_code, ac: AsyncClient):
#     response = await ac.post("/auth/register", json={
#         "email": email,
#        "password": password
#     }) 
#     assert response.status_code == status_code
    
    
# @pytest.mark.parametrize("email, password, status_code", [
#     ("test@test.com", "test", 200),
#     ("artem@example.com", "artem", 200)
# ])
# async def test_login_user(email, password, status_code, ac: AsyncClient):
#     response = await ac.post("/auth/login", json={
#         "email": email,
#         "password": password,
        
#     })
#     assert response.status_code == status_code