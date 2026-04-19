import pytest
from datetime import date
from tests.conftest import UserAchievementsTestDAO, AchievementTestDAO, UserAchievementsTest


class TestUserAchievementsDAO:

    async def test_find_user_all_return_all_user_achievements(self, db_session, sample_user_achievement):
        """UserAchievementsDAO.find_user_all(): должен вернуть все достижения пользователя"""
        achievement, user=sample_user_achievement
        result=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=user.id)
        assert len(result)==1
        assert achievement.id in [a.id for a in result]
    
    async def test_find_user_all_returns_correct_type(self, db_session, sample_user):
        """UserAchievementsDAO.find_user_all(): возвращает список моделей UserAchievements"""
        achievement=await AchievementTestDAO.add(
            session=db_session,
            name="sample",
            description="sample",
            type="sampleType",
            goal=10
        )
        await UserAchievementsTestDAO.add(
            session=db_session,
            user_id=sample_user.id,
            achievement_id=achievement.id
        )
        result=await UserAchievementsTestDAO.find_user_all(
            session=db_session,
            user_id=sample_user.id
        )
        assert isinstance(result, list)
        assert all(isinstance(item, UserAchievementsTest) for item in result)

