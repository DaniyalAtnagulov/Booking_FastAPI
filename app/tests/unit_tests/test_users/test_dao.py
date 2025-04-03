import pytest
from app.users.dao import UsersDAO

@pytest.mark.parametrize("user_id,email,is_present", [
    (1, "test@test.com", True),
    (2, "artem@example.com", True),
    (3, "...", False )
])
async def test_find_user_by_id(user_id, email, is_present):
    user = await UsersDAO.find_by_id(user_id)
    
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
        
"""Важно запускать именно этот файл, так как иначе в test_api у нас создаться user c user.id = 3 и тесты не пройдут
pytest -v -s app/tests/unit_tests/test_users/test_dao.py """        