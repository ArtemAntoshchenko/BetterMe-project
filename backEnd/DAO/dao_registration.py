from .dao_base import BaseDAO
from ..db.models import User
from ..db.database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserDAO(BaseDAO):
    model=User

    @classmethod
    async def changeUserStatus(cls, user_id, session: AsyncSession=None):
        if session:
            query=select(cls.model).where(cls.model.id==user_id)
            user=await session.scalar(query)
            if user:
                user.super_user=True
                await session.flush()
                return user
            else:
                return None
        async with get_db() as new_session:
            query=select(cls.model).where(cls.model.id==user_id)
            user=await new_session.scalar(query)
            if user:
                user.super_user=True
                await new_session.flush()
                return user
            else:
                return None
    @classmethod
    async def find_superusers(cls, session: AsyncSession=None):
        if session:
            query=select(cls.model).where(cls.model.super_user==True)
            superusers=await session.scalars(query)
            return superusers.all()
        async with get_db() as new_session:
            query=select(cls.model).where(cls.model.super_user==True)
            superusers=await new_session.scalars(query)
            return superusers.all()

        