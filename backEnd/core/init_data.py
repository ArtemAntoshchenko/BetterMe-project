from datetime import datetime
from ..core.auth import get_password_hash
from sqlalchemy import select
from ..db.database import get_db
from ..db.models import User
from ..DAO.dao_registration import UserDAO
from .config import settings
import getpass

async def init_superuser():
        result=await UserDAO.find_superuser()
        if result:
            print(f"Суперпользователь уже существует: {result.nickname} ({result.login})")
            return
        
        print("="*30)
        print("СОЗДАНИЕ ПЕРВОГО СУПЕРПОЛЬЗОВАТЕЛЯ")
        print(f"Никнейм: {settings.SUPERUSER_NICKNAME}")
        print(f"Логин: {settings.SUPERUSER_LOGIN}")
        print("="*30)
        password=getpass.getpass("Введите пароль для суперпользователя: ")
        password_confirm=getpass.getpass("Подтвердите пароль: ")
        if password!=password_confirm:
            print("Пароли не совпадают!")
            return
        if len(password)<6:
            print("Пароль должен быть не менее 6 символов!")
            return
        
        try:
            hashed_password=get_password_hash(password)
            superuser_data={
                'nickname':settings.SUPERUSER_NICKNAME,
                'login':settings.SUPERUSER_LOGIN,
                'password':hashed_password,
                'email':settings.SUPERUSER_EMAIL,
                'phone_number':settings.SUPERUSER_PHONE,
                'first_name':settings.SUPERUSER_FIRST_NAME,
                'last_name':settings.SUPERUSER_LAST_NAME,
                'city':settings.SUPERUSER_CITY,
                'date_of_birth':datetime.strptime(settings.SUPERUSER_DATE_OF_BIRTH, "%Y-%m-%d").date(),
                'super_user':True
            }
            await UserDAO.add(**superuser_data) 
        except Exception as e:
            print(f"Ошибка при создании суперпользователя: {e}")
            raise