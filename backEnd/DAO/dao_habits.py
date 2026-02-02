from .dao_base import BaseDAO
from ..db.models import Habit
from ..db.database import get_db
from sqlalchemy import select
 
class HabitDAO(BaseDAO):
    model=Habit

    @classmethod
    async def find_all_active(cls):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.complit==False)
            result=await session.scalars(query)
            result_list=result.all()
            return result_list
        
    @classmethod
    async def complit_habit(cls, habit_id):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.id==habit_id)
            habit=await session.scalar(query)
            habit.progress=min(habit.progress+habit.step, habit.goal)
            habit.complit_today=True
            return habit