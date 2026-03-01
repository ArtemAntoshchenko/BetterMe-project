from pydantic import BaseModel, Field, ConfigDict

class CreateAchievementSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    name: str=Field(..., min_length=1, max_length=20, description="Название достижения")
    description: str=Field(..., min_length=1, max_length=300, description="Описание достижения")
    