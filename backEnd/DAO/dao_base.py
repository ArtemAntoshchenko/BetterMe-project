from typing import Generic, TypeVar, Type
from db.database import Base, get_db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

ModelType = TypeVar("ModelType", bound=Base)

class BaseDAO(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model=model

    async def find_one_or_none(self, **filters):
        async with get_db() as session:
            query=select(self.model).filter_by(**filters)
            result=await session.execute(query)
            return result.scalar_one_or_none()  
        
    async def add(self, **values):
        async with get_db() as session:
            new_instance = self.model(**values)
            session.add(new_instance)
            await session.flush()
            return new_instance