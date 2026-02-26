from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re
from datetime import date, datetime
from typing import Optional


class ProfileUpdateSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id: int
    nickname: str=Field(..., min_length=1, max_length=15, description="Никнейм, от 1 до 15 знаков")
    password: str=Field(..., min_length=6, max_length=30, description="Пароль, от 6 до 30 знаков")
    email: EmailStr=Field(..., description="Электронная почта")
    phone_number: str=Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    city: str=Field(..., min_length=3, max_length=20, description="Название города, от 3 до 20 символов")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{11}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать 11 цифр')
        return value
    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str) -> str:
        new_value=value.capitalize()
        return new_value
    
class ProfileUpdateResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    
    id: int
    nickname: str=Field(..., min_length=1, max_length=15, description="Никнейм, от 1 до 15 знаков")
    email: EmailStr=Field(..., description="Электронная почта")
    phone_number: str=Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    city: str=Field(..., min_length=3, max_length=20, description="Название города, от 3 до 20 символов")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{11}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать 11 цифр')
        return value
    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str) -> str:
        new_value=value.capitalize()
        return new_value
