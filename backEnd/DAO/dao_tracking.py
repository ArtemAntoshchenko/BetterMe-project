from .dao_base import BaseDAO
from ..db.models import HabitCompletion
from ..db.database import get_db
from ..schemas.model_schemas.habit_schema import HabitCompletionSchema
from sqlalchemy import select
from datetime import date, timedelta

class TrackingDAO(BaseDAO):
    model=HabitCompletion

    @classmethod
    async def calculate_current_streak(cls, habit_id: int, check_date: date=date.today())-> int:
        async with get_db() as session:
            query=select(cls.model.completed_date).where(
                cls.model.habit_id==habit_id, 
                cls.model.completed_date>=check_date
                ).order_by(cls.model.completed_date.desc())
            result=await session.scalars(query)
            completed_dates=set(result.all())
            streak=0
            current_date=check_date
            while current_date in completed_dates:
                streak+=1
                current_date-=timedelta(days=1)
            return streak
        
    @classmethod
    async def create_completion(cls, habit_id: int, user_id: int)-> HabitCompletionSchema:
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
        async def get_heatmap_data(cls, habit_id: int, days: int=365)->Dict[str, int]:
            today=date.today()
            start_date=today-timedelta(days=days-1)
            async with get_db() as session:
                query=select(cls.model.completed_date).where(
                    cls.model.habit_id==habit_id,
                    cls.model.completed_date>=start_date,
                    cls.model.completed_date<=today
                ).order_by(cls.model.completed_date)
            result=await session.scalars(query)
            completed_dates=set(result.all())
            heatmap={}
            current=start_date
            while current<=today:
                date_str=current.isoformat()
                heatmap[date_str]=1 if current in completed_dates else 0
                current+=timedelta(days=1)
            return heatmap
        
        @classmethod
        async def get_heatmap_stats(cls, habit_id: int, days: int=365)-> dict:
            today=date.today()
            start_date=today-timedelta(days=days-1)
            async with get_db() as session:
                completions=select(cls.model.completed_date).where(
                    cls.model.habit_id==habit_id,
                    cls.model.completed_date>=start_date,
                    cls.model.completed_date<=today
                ).order_by(cls.model.completed_date)
                completions_list=completions.all()
                if not completions_list:
                    return {
                        'current_streak': 0,
                        'longest_streak': 0,
                        'total_completions': 0,
                        'completion_rate': 0
                    }
                
                last=completions_list[-1]
                completion_rate=round((len(completions_list)/days)*100, 1)
                return {
                'current_streak': last.current_streak,
                'longest_streak': last.longest_streak,
                'total_completions': len(completions_list),
                'completion_rate': completion_rate
                }
