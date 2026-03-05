from pydantic import BaseModel, Field, ConfigDict

class AchievementTypeResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    value: str=Field(..., min_length=1, max_length=50)
    label: str=Field(..., min_length=1, max_length=50)
