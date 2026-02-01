from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class HabitSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    name: str=Field(..., description="Имя привычки")
    description: str=Field(..., max_length=300, description="Описание привычки")
    complit: Optional[bool]=Field(None, description="Состояние привычки")
    complit_today: Optional[bool]=Field(None, description="Состояние привычки на сегодня")
    goal: int=Field(..., description="Цель для привычки")
    progress: Optional[int]=Field(None, description="Прогресс привычки")
    step: int=Field(..., description="Шаг выполнения привычки")