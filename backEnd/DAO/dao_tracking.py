from .dao_base import BaseDAO
from .dao_habits import HabitDAO  
from ..db.models import HabitCompletion
from ..db.database import get_db
from ..schemas.model_schemas.completion_habit_schema import HabitCompletionSchema
from sqlalchemy import select
from datetime import date, timedelta
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

class TrackingDAO(BaseDAO):
    model = HabitCompletion

    @classmethod
    async def calculate_current_streak(cls, habit_id: int, check_date: date=date.today(), 
                                    session: AsyncSession=None)-> int:
        async def _execute(sess):
            query = select(cls.model.completed_date).where(
                cls.model.habit_id==habit_id, 
                cls.model.completed_date>=check_date
            ).order_by(cls.model.completed_date.desc())
            result = await sess.scalars(query)
            return set(result.all())
        if session:
            completed_dates=await _execute(session)
        else:
            async with get_db() as new_session:
                completed_dates=await _execute(new_session)
        streak=0
        current_date=check_date
        while current_date in completed_dates:
            streak+=1
            current_date-=timedelta(days=1)
        return streak

    @classmethod
    async def get_heatmap_data(cls, habit_id: int, days: int = 365, 
                            session: AsyncSession = None) -> Dict[str, int]:
        today = date.today()
        start_date = today - timedelta(days=days-1)
        
        async def _execute(sess):
            query = select(cls.model.completed_date).where(
                cls.model.habit_id == habit_id,
                cls.model.completed_date >= start_date,
                cls.model.completed_date <= today
            ).order_by(cls.model.completed_date)
            result = await sess.scalars(query)
            return set(result.all())
        
        if session:
            completed_dates = await _execute(session)
        else:
            async with get_db() as new_session:
                completed_dates = await _execute(new_session)
        
        heatmap = {}
        current = start_date
        while current <= today:
            date_str = current.isoformat()
            heatmap[date_str] = 1 if current in completed_dates else 0
            current += timedelta(days=1)
        return heatmap

    @classmethod
    async def get_heatmap_stats(cls, habit_id: int, days: int = 365,
                               session: AsyncSession = None) -> dict:
        today = date.today()
        start_date = today - timedelta(days=days-1)
        
        async def _execute(sess):
            query = select(cls.model).where(
                cls.model.habit_id == habit_id,
                cls.model.completed_date >= start_date,
                cls.model.completed_date <= today
            ).order_by(cls.model.completed_date)
            result = await sess.scalars(query)
            return result.all()
        
        if session:
            completions_list = await _execute(session)
        else:
            async with get_db() as new_session:
                completions_list = await _execute(new_session)
        
        if not completions_list:
            return {
                'total_completions': 0,
                'completion_rate': 0,
                'current_streak': 0,
                'longest_streak': 0
            }
        
        last = completions_list[-1]
        completion_rate = round((len(completions_list) / days) * 100, 1)
        return {
            'current_streak': last.current_streak,
            'longest_streak': last.longest_streak,
            'total_completions': len(completions_list),
            'completion_rate': completion_rate
        }

    @classmethod
    async def get_all_habits_heatmap_data(cls, days: int = 90) -> List[dict]:
        # Используем ОДНУ сессию для всего
        async with get_db() as session:
            # Передаем сессию в HabitDAO
            habits = await HabitDAO.find_all_active(session=session)
            
            result = []
            for habit in habits:
                # Передаем ту же сессию во все методы
                heatmap_data = await cls.get_heatmap_data(habit.id, days, session=session)
                stats = await cls.get_heatmap_stats(habit.id, days, session=session)
                
                hue = (habit.id * 137) % 360
                result.append({
                    'habit_id': habit.id,
                    'habit_name': habit.name,
                    'color': f"hsl({hue}, 70%, 50%)",
                    'heatmap_data': heatmap_data,
                    'current_streak': stats['current_streak'],
                    'total_completions': stats['total_completions']
                })
            
            return result