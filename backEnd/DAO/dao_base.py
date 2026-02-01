from ..db.database import Base, get_db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, delete 

class BaseDAO():
    model=None

    @classmethod
    async def find_all(cls):
        async with get_db() as session:
            query=select(cls.model)
            result=await session.scalars(query)
            result_list=result.all()
            return result_list
        
    @classmethod
    async def find_one_or_none(cls, **filters):
        async with get_db() as session:
            query=select(cls.model).filter_by(**filters)
            result=await session.execute(query)
            return result.scalar_one_or_none()
              
    @classmethod 
    async def add(cls, **values):
        async with get_db() as session:
            new_instance=cls.model(**values)
            session.add(new_instance)
            await session.flush()
            return new_instance

    @classmethod
    async def update(cls, filter_by: dict, **values):
        async with get_db() as session:
            query=(
                update(cls.model)
                .where(*[
                    getattr(cls.model, key)==value 
                    for key, value in filter_by.items()
                ])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            select_query=select(cls.model).where(*[
                getattr(cls.model, key)==value 
                for key, value in filter_by.items()
            ])
            result=await session.execute(select_query)
            updated_record=result.scalar_one_or_none()
            return updated_record
    
    @classmethod
    async def delete(cls, delete_all: bool=False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления!")
        async with get_db() as session:
            query=delete(cls.model).filter_by(**filter_by)
            result=await session.execute(query)
            return result.rowcount