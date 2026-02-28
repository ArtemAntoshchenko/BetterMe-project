from .dao_base import BaseDAO
from ..db.models import User
from ..db.database import get_db
from sqlalchemy import select
 
class UserDAO(BaseDAO):
    model=User

    @classmethod
    async def changeUserStatus(cls, user_id):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.id==user_id)
            user=await session.scalar(query)
            user.super_user=True
            return user
        
    @classmethod
    async def find_superuser(cls):
        async with get_db() as session:
            query=select(cls.model).where(cls.model.super_user==True)
            superuser=await session.scalar(query)
            return superuser