from .dao_base import BaseDAO
from ..db.models import UserAchievements
from ..db.database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserAchievementsDAO(BaseDAO):
    model=UserAchievements
 
    @classmethod
    async def find_user_all(cls, user_id, session: AsyncSession=None):
        if session:
            query=select(cls.model).where(cls.model.user_id==user_id)
            result=await session.scalars(query)
            result_list=result.all()
            return result_list
        async with get_db() as new_session:
            query=select(cls.model).where(cls.model.user_id==user_id)
            result=await new_session.scalars(query)
            result_list=result.all()
            return result_list
        