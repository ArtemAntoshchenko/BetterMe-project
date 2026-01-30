from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re
from datetime import date, datetime


class UserRegisterSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    email: EmailStr=Field(..., description="Электронная почта")
    login: str=Field(..., min_length=4, max_length=15, description="Логин, от 4 до 15 знаков")
    password: str=Field(..., min_length=6, max_length=30, description="Пароль, от 6 до 30 знаков")
    phone_number: str=Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str=Field(..., min_length=2, max_length=20, description="Имя, от 2 до 20 символов")
    last_name: str=Field(..., min_length=2, max_length=20, description="Фамилия, от 2 до 20 символов")
    city: str=Field(..., min_length=3, max_length=20, description="Название города, от 3 до 20 символов")
    date_of_birth: date=Field(..., description="Дата рождения в формате ГГГГ-ММ-ДД")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{11}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать 11 цифр')
        return value
    @field_validator("city")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not value[0].isupper():
            raise ValueError('Название города должно начинаться с заглавной буквы')
        return value
    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value and value>=datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value

class UserAuthSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    login: str=Field(...,  min_length=4, max_length=15, description="Логин для входа")
    password: str=Field(..., min_length=6, max_length=30, description="Пароль, от 6 до 30 знаков")