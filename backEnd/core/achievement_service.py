from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import select, func
from ..db.database import get_db
from ..DAO.dao_registration import UserDAO
from ..DAO.dao_tracking import TrackingDAO
from ..DAO.dao_user_achievements import UserAchievementsDAO
from ..DAO.dao_achievement import AchievementDAO
from ..db.models import User, Achievement


class AchievementTypes:
    PROFILE_FILLED="profile_filled"
    LONGEST_STREAK="longest_streak"

    @classmethod
    def get_all_types(cls):
        return [
            {"value": cls.PROFILE_FILLED, "label": "Заполнение профиля"},
            {"value": cls.LONGEST_STREAK, "label": "Самый длинный стрик"}
        ]

class AchievementService:
    
    @classmethod
    async def check_and_award_achievements(cls, user_id: int)-> List[Achievement]:
        user=await UserDAO.find_one_or_none(id=user_id)
        if not user:
            return []
        all_achievements=await AchievementDAO.find_all()
        user_achievements=await UserAchievementsDAO.find_user_all(user_id=user_id)
        earned_achievements={user_achievement.achievement_id for user_achievement in user_achievements}
        new_achievements=[]
        for achievement in all_achievements:
            if achievement.id in earned_achievements:
                continue 
            if await cls._check_achievement_condition(user, achievement):
                new_achievement=await UserAchievementsDAO.add(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                new_achievements.append(achievement)
        return new_achievements
    
    @classmethod
    async def _check_achievement_condition(cls, user: User, achievement: Achievement)-> bool:
        if achievement.type==AchievementTypes.PROFILE_FILLED:
            return cls._check_profile_filled(user, achievement) 
        elif achievement.type==AchievementTypes.LONGEST_STREAK:
            return await cls._check_longest_streak(user, achievement)
        return False
    
    @classmethod
    def _check_profile_filled(cls, user: User, achievement: Achievement)-> bool:
        fields_to_check=[
            user.nickname,
            user.login,
            user.password,
            user.date_of_birth,
            user.first_name,
            user.last_name,
            user.city,
            user.phone_number,
            user.email,
        ]
        filled_fields=sum(
            1 for field in fields_to_check 
            if field and str(field).strip()
            )
        if achievement.goal>0:
            return filled_fields>=achievement.goal
        else:
            return filled_fields>=len(fields_to_check)
        
    @classmethod
    async def _check_longest_streak(cls, user: User, achievement: Achievement)-> bool:
        streak=await TrackingDAO.get_user_longest_streak(user_id=user.id)
        return streak>=achievement.goal if achievement.goal>0 else False