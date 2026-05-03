from ..db.database import Base, get_db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO():
    model=None

    @classmethod
    async def find_all(cls, session: AsyncSession=None):
        if session:
            query=select(cls.model)
            result=await session.scalars(query)
            return result.all()
        async with get_db() as new_session:
            query=select(cls.model)
            result=await new_session.scalars(query)
            return result.all()
        
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession=None, **filters):
        if session:
            query=select(cls.model).filter_by(**filters)
            result=await session.execute(query)
            return result.scalar_one_or_none()
        async with get_db() as new_session:
            query=select(cls.model).filter_by(**filters)
            result=await new_session.execute(query)
            return result.scalar_one_or_none()
              
    @classmethod
    async def add(cls, session: AsyncSession=None, **values):
        if session:
            new_instance=cls.model(**values)
            session.add(new_instance)
            await session.flush()
            return new_instance
        async with get_db() as new_session:
            new_instance=cls.model(**values)
            new_session.add(new_instance)
            await new_session.flush()
            return new_instance

    @classmethod
    async def update(cls, filter_by: dict, session: AsyncSession=None, **values):
        if session:
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
        async with get_db() as new_session:
            query=(
                update(cls.model)
                .where(*[
                    getattr(cls.model, key)==value 
                    for key, value in filter_by.items()
                ])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            await new_session.execute(query)
            select_query=select(cls.model).where(*[
                getattr(cls.model, key)==value 
                for key, value in filter_by.items()
            ])
            result=await new_session.execute(select_query)
            updated_record=result.scalar_one_or_none()
            return updated_record
    
    @classmethod
    async def delete(cls, delete_all: bool=False, session: AsyncSession=None, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления!")
        if session: 
            query=select(cls.model).filter_by(**filter_by)
            result=await session.execute(query)
            objects=result.scalars().all()
            for obj in objects:
                await session.delete(obj)
            await session.flush()
            return len(objects)
        async with get_db() as new_session:
            query=select(cls.model).filter_by(**filter_by)
            result=await new_session.execute(query)
            objects=result.scalars().all()
            for obj in objects:
                await new_session.delete(obj)
            await new_session.flush()
            return len(objects)