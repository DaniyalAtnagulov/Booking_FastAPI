from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
# В версии Pydantic 2.0 модуль BaseSettings 
# был вынесен в отдельную библиотеку pydantic-settings. 
# Необходимо установить ее для корректной работы через pip install pydantic-settings

class Settings(BaseSettings): #принимает все параметры 
    
    MODE: Literal["DEV",  "TEST", "PROD"] #Literal  проверяет что значание являеся одним из вариатов в скобках
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"#создаются динамически параметры и перменные
    # Возможно имеет смысл поискать спосособ сделать это более лаконично? а не повтряться, доьавляя переменным префис TEST"""
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def DATABASE_TEST_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
 
    SMTP_HOST: str
    SMTP_PORT: int 
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    # Со 2 версии Pydantic, class Config был заменен на атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() #по итогу мы создали данный файл, котрый принимает папраметры(DB_HOST и т.д.) 
# создет динамические параметры и перменные и по итогу все это аккумулируется в единственной перменной settings 
# к которой теперь будем часто обращаться в других файлах


#print(settings.DB_HOST) 
#print(settings.DATABASE_URL) чисто для проверки передались ли данные из .env раскомметировать и написать
# в консоли находясь в главной директории(PS C:\Users\Professional\Desktop\FASTAPI_NEWEST>) python app/config.py