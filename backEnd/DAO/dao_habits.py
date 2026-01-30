from .dao_base import BaseDAO
from ..db.models import Habit
from ..db.database import get_db
from sqlalchemy import select
 
class HabitDAO(BaseDAO[Habit]):
    def __init__(self):
        super().__init__(Habit)
    
    async def find_all_active(self):
        async with get_db() as session:
            query=select(self.model).where(self.model.active==True)
            result=await session.scalars(query)
            result_list=result.all()
            return result_list 