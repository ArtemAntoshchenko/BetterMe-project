from pydantic import BaseModel, Field, model_validator


class HabitCreateSchema(BaseModel):
    name: str=Field(..., min_length=1, max_length=20, description="Имя привычки")
    description: str=Field(..., max_length=300, description="Описание привычки")
    goal: int=Field(..., gt=0, description="Цель для привычки")
    step: int=Field(..., gt=0, description="Шаг выполнения привычки")

    @model_validator(mode='after')
    def validate_step(self)-> 'HabitCreateSchema':
        if self.goal%self.step==0:
            return self
        else:
            raise ValueError('Значение шага должно быть кратно значению цели!')