from pydantic import BaseModel, Field, ConfigDict

class AchievementSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str=Field(..., description="Название достижения")
    description: str=Field(..., max_length=300, description="Описание достижения")
    obtained: bool=Field(..., default=False, description="Состояние достижения")
    