from .dao_base import BaseDAO
from ..db.models import Achievement
from ..db.database import get_db
from sqlalchemy import select
from datetime import date, timedelta
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

class AchievementDAO(BaseDAO):
    model=Achievement

    @classmethod
    async def obtain_achievement(cls, achievement_id, user_id):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.id==achievement_id, cls.model.user_id==user_id)
            achievement=await session.scalar(query)
            achievement.obtained=True
            return achievement
        
    @classmethod
    async def find_user_all(cls, user_id):
        async with get_db() as session:
            query=select(cls.model).where(user_id==user_id)
            result=await session.scalars(query)
            result_list=result.all()
            return result_list
        
