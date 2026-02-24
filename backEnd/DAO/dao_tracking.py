from .dao_base import BaseDAO
from .dao_habits import HabitDAO  
from ..db.models import HabitCompletion
from ..db.database import get_db
from ..schemas.model_schemas.create_completion_schema import CreateCompletionSchema
from sqlalchemy import select
from datetime import date, timedelta
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

class TrackingDAO(BaseDAO):
    model=HabitCompletion

    @classmethod
    async def create_completion(cls, habit_id: int, user_id: int)-> CreateCompletionSchema:
        today=date.today()
        async with get_db() as session:
            existing=await session.scalar(
                select(cls.model).where(
                    cls.model.habit_id==habit_id,
                    cls.model.completed_date==today
                )
            )
            if existing:
                raise ValueError("Привычка уже отмечена сегодня")
            last_completion=await session.scalar(
                select(cls.model).where(
                    cls.model.habit_id==habit_id
                ).order_by(cls.model.completed_date.desc())
            )
            if last_completion and last_completion.completed_date==today-timedelta(days=1):
                current_streak=last_completion.current_streak+1
            else:
                current_streak=1
            longest_streak=max(current_streak, last_completion.longest_streak) if last_completion else current_streak
            new_completion=cls.model(
                habit_id=habit_id,
                user_id=user_id,
                completed_date=today,
                current_streak=current_streak,
                longest_streak=longest_streak
            )
            session.add(new_completion)
            return new_completion

    @classmethod
    async def get_heatmap_data(cls, habit_id: int, days: int=365, 
                            session: AsyncSession=None)-> Dict[str, int]:
        today=date.today()
        start_date=today-timedelta(days=days-1)
        async def _execute(session):
            query=select(cls.model.completed_date).where(
                cls.model.habit_id==habit_id,
                cls.model.completed_date>=start_date,
                cls.model.completed_date<=today
            ).order_by(cls.model.completed_date)
            result=await session.scalars(query)
            return set(result.all())
        if session:
            completed_dates=await _execute(session)
        else:
            async with get_db() as new_session:
                completed_dates=await _execute(new_session)
        heatmap={}
        current=start_date
        while current<=today:
            date_str=current.isoformat()
            heatmap[date_str]=1 if current in completed_dates else 0
            current+=timedelta(days=1)
        return heatmap

    @classmethod
    async def get_heatmap_stats(cls, habit_id: int, days: int=365,
                               session: AsyncSession=None)-> dict:
        today=date.today()
        start_date = today-timedelta(days=days-1)
        async def _execute(session):
            query=select(cls.model).where(
                cls.model.habit_id==habit_id,
                cls.model.completed_date>=start_date,
                cls.model.completed_date<=today
            ).order_by(cls.model.completed_date)
            result=await session.scalars(query)
            return result.all()
        if session:
            completions_list=await _execute(session)
        else:
            async with get_db() as new_session:
                completions_list=await _execute(new_session)
        if not completions_list:
            return {
                'total_completions': 0,
                'completion_rate': 0,
                'current_streak': 0,
                'longest_streak': 0
            }
        last=completions_list[-1]
        completion_rate=round((len(completions_list)/days)*100, 1)
        return {
            'current_streak': last.current_streak,
            'longest_streak': last.longest_streak,
            'total_completions': len(completions_list),
            'completion_rate': completion_rate
        }

    @classmethod
    async def get_all_habits_heatmap_data(cls, days: int=90)-> List[dict]:
        async with get_db() as session:
            habits=await HabitDAO.find_all_active(session=session)
            result=[]
            for habit in habits:
                heatmap_data=await cls.get_heatmap_data(habit.id, days, session=session)
                stats=await cls.get_heatmap_stats(habit.id, days, session=session)
                hue=(habit.id * 137)%360
                result.append({
                    'habit_id': habit.id,
                    'habit_name': habit.name,
                    'color': f"hsl({hue}, 70%, 50%)",
                    'heatmap_data': heatmap_data,
                    'current_streak': stats['current_streak'],
                    'total_completions': stats['total_completions']
                })
            return result