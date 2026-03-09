from datetime import datetime
from ..core.auth import get_password_hash
from sqlalchemy import select
from ..db.database import get_db, engine, Base
from sqlalchemy.exc import OperationalError, ProgrammingError
from ..db.models import User
from ..DAO.dao_registration import UserDAO
from .config import settings
import getpass
import asyncio
import os

async def init_superuser():
    max_retries=10
    retry_delay=3 
    for attempt in range(max_retries):
        try:
            print(f"Попытка создания таблиц ({attempt+1}/{max_retries})...")
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы или уже существуют")
            result=await UserDAO.find_superuser()
            if result:
                print(f"Суперпользователь уже существует: {result.nickname} ({result.login})")
                return
            print("="*30)
            print("СОЗДАНИЕ ПЕРВОГО СУПЕРПОЛЬЗОВАТЕЛЯ")
            print(f"Никнейм: {settings.SUPERUSER_NICKNAME}")
            print(f"Логин: {settings.SUPERUSER_LOGIN}")
            print("="*30)
            password=os.getenv("SUPERUSER_PASSWORD", "admin123")
            try:
                hashed_password = get_password_hash(password)
                superuser_data = {
                    'nickname': settings.SUPERUSER_NICKNAME,
                    'login': settings.SUPERUSER_LOGIN,
                    'password': hashed_password,
                    'email': settings.SUPERUSER_EMAIL,
                    'phone_number': settings.SUPERUSER_PHONE,
                    'first_name': settings.SUPERUSER_FIRST_NAME,
                    'last_name': settings.SUPERUSER_LAST_NAME,
                    'city': settings.SUPERUSER_CITY,
                    'date_of_birth': datetime.strptime(settings.SUPERUSER_DATE_OF_BIRTH, "%Y-%m-%d").date(),
                    'super_user': True
                }
                await UserDAO.add(**superuser_data)
                print("Суперпользователь успешно создан!")
                return 
            except Exception as e:
                print(f"Ошибка при создании суперпользователя: {e}")
                raise
        except (OperationalError, ProgrammingError, ConnectionRefusedError) as e:
            if "Connection refused" in str(e) or "does not exist" in str(e):
                if attempt<max_retries-1:
                    print(f"База данных еще не готова. Ошибка: {e}")
                    print(f"Повторная попытка через {retry_delay} секунд...")
                    await asyncio.sleep(retry_delay)
                else:
                    print(f"Не удалось подключиться к базе данных после {max_retries} попыток")
                    raise e
            else:
                raise
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            raise