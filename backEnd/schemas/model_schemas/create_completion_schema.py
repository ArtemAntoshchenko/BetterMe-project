from typing import Optional, Dict, List
from pydantic import BaseModel, Field, ConfigDict

class CreateCompletionSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    habit_id: int
    user_id: int
    completed_date: int=Field(..., description='Дата выполнения привычки')
    current_streak: int=Field(..., description="Стрик")
    longest_streak: int=Field(..., description="Самый длинный стрик")