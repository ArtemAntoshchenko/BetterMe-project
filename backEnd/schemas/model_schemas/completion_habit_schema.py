from typing import Optional, Dict, List
from pydantic import BaseModel, Field, ConfigDict

class HabitCompletionSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    habit_id: int
    user_id: int
    habit_name: str=Field(..., description="Название привычки")
    habit_description: Optional[str]=Field(None, max_length=300, description="Описание привычки")
    goal: Optional[int]=Field(None, description="Цель для привычки")
    progress: int=Field(..., description="Прогресс привычки")
    step: Optional[int]=Field(None, description="Шаг выполнения привычки")
    heatmap_data: Dict[str, int]=Field(..., description="Данные для графика")
    current_streak: int=Field(..., description="Стрик")
    longest_streak: int=Field(..., description="Самый длинный стрик")
    completion_rate: float=Field(..., description="Частота выполнения привычек")

class AllHabitsCompletionSchema(BaseModel):
    habits: List[dict]