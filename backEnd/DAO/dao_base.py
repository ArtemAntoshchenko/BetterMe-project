from typing import Generic, TypeVar, Type
from ..db.database import Base, get_db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, delete 

ModelType = TypeVar("ModelType", bound=Base)

class BaseDAO(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model=model

    async def find_all(self):
        async with get_db() as session:
            query=select(self.model)
            result=await session.scalars(query)
            result_list=result.all()
            return result_list
        
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

    async def update(self, filter_by: dict, **values):
        async with get_db() as session:
            query=(
                update(self.model)
                .where(*[
                    getattr(self.model, key) == value 
                    for key, value in filter_by.items()
                ])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            result=await session.execute(query)
            return result
    
    async def delete(self, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления!")
        async with get_db() as session:
            query=delete(self.model).filter_by(**filter_by)
            result=await session.execute(query)
            return result.rowcount