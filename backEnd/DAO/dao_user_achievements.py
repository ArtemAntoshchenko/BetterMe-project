from .dao_base import BaseDAO
from ..db.models import UserAchievements
from ..db.database import get_db
from sqlalchemy import select

class UserAchievementsDAO(BaseDAO):
    model=UserAchievements

    @classmethod
    async def obtain_achievement(cls, achievement_id, user_id):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.achievement_id==achievement_id, cls.model.user_id==user_id)
            achievement=await session.scalar(query)
            achievement.obtained=True
            return achievement
        