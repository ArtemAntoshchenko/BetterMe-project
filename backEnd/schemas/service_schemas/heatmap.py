from pydantic import BaseModel
from datetime import date
from typing import Dict, Optional

class HabitHeatmapResponse(BaseModel):
    habit_id: int
    habit_name: str
    habit_description: Optional[str]
    goal: Optional[int]
    progress: int
    step: Optional[int]
    heatmap_data: Dict[str, int] 
    current_streak: int
    longest_streak: int
    total_completions: int
    completion_rate: float