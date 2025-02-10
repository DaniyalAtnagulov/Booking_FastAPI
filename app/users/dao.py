from app.dao.base import BaseDAO
from app.users.model import Users


class UsersDAO(BaseDAO):
    model = Users