from .dao_base import BaseDAO
from ..db.models import Habit
from ..db.database import get_db
from sqlalchemy import select
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

class HabitDAO(BaseDAO):
    model=Habit

    @classmethod
    async def find_all_active(cls, session: AsyncSession=None):
        async def _execute(alt_session):
            query=select(cls.model).where(cls.model.complit==False)
            result=await alt_session.scalars(query)
            return result.all()
        if session:
            return await _execute(session)
        else:
            async with get_db() as new_session:
                return await _execute(new_session)
        
    @classmethod
    async def complit_habit(cls, habit_id, user_id):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.id==habit_id, cls.model.user_id==user_id)
            habit=await session.scalar(query)
            habit.progress=min(habit.progress+habit.step, habit.goal)
            habit.complit_today=True
            return habit
        
    @classmethod
    async def daily_habit_status_update(cls, habit_id):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.id==habit_id)
            habit=await session.scalar(query)
            time_since_update=datetime.now()-habit.updated_at
            if time_since_update>=timedelta(days=1):
                habit.complit_today=False
                habit.updated_at=datetime.now()
                return 'Статус привычек был обновлен'
            else:
                return 'Еще не прошли сутки с последнего обновления'