import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from tests.conftest import UserAchievementsTestDAO, AchievementTestDAO, UserAchievementsTest


class TestUserAchievementsDAO:

    async def test_find_user_all_return_all_user_achievements_bonds(self, db_session, sample_user_achievement):
        """UserAchievementsDAO.find_user_all(): должен вернуть все связи достижений и пользователя"""
        achievement, user=sample_user_achievement
        result=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=user.id)
        assert len(result)==1
        assert achievement.id in [a.achievement_id for a in result]
    
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
        result=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=sample_user.id)
        assert isinstance(result, list)
        assert all(isinstance(i, UserAchievementsTest) for i in result)

    async def test_find_user_all_empty_for_user_without_achievements(self, db_session, sample_user):
        """UserAchievementsDAO.find_user_all(): возвращает пустой список для пользователя без достижений"""
        result=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=sample_user.id)
        assert isinstance(result, list)
        assert result==[]
    
    async def test_find_user_all_with_nonexistent_user(self, db_session):
        """UserAchievementsDAO.find_user_all(): возвращает пустой список для несуществующего пользователя"""
        result=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=99)
        assert isinstance(result, list)
        assert result==[]

    async def test_find_user_all_respects_unique_constraint(self, db_session, sample_user):
        """UserAchievementsDAO.find_user_all(): соблюдает unique constraint"""
        achievement=await AchievementTestDAO.add(
            session=db_session,
            name="sample",
            description="sample",
            type="sampleType",
            goal=10
        )
        first=await UserAchievementsTestDAO.add(
            session=db_session,
            user_id=sample_user.id,
            achievement_id=achievement.id
        )
        assert first is not None
        with pytest.raises(IntegrityError):
            await UserAchievementsTestDAO.add(
                session=db_session,
                user_id=sample_user.id,
                achievement_id=achievement.id
            )




