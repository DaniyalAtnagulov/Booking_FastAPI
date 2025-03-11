from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from app.config import settings

from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str: #функция принимает словарь, а возвращает jwt, котор является строкой
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30) # тут только токен доступа, рефреш-токен не реализован, посему пользолвателя выкидывает через 30 мин
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM      #aslaasdawd - секретный ключ в виде рандомной строки в дальнейшем его сгенерирую специальным скриптом, а пока просто от руки задал
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):                       
    user = await UsersDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):  
        return None
    return user
    
# Асинхронные функции используем, где есть обращение к базе данных, чтение/запись файла - в общем, любая операция, 
# в которой нужно ждать ответа от внешнего сервиса (Базы данных, операционной системы или другого сервиса). 
# Там, где нет обращения к чужому сервису, используем синхронные функции. Например, для функции по хэшированию пароля    
    
    