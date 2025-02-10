# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

# def get_password_hash(password:str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def create_accsess_token(data: dict) -> str: #функция принимает словарь, а возвращает jwt, котор является строкой
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=30) # тут только токен доступа, рефреш-токен не реализован, посему пользолвателя выкидывает через 30 мин
#     to_encode.update({"exp":expire})
#     encoded_jwt = jwt.encode(
#         to_encode,"aslaasdawd", "HS256"      #aslaasdawd - секретный ключ в виде рандомной строки в дальнейшем его сгенерирую специальным скриптом, а пока просто от руки задал
#     )
#     return encoded_jwt
    
    
        









# # print(get_password_hash('aaaa'))
# # print(verify_password('aaaa','$2b$12$iTzj7o6gGEU.nPJjAaWQeO80wdAz4f8kt2KoWJH9IptNELouplPcO'))