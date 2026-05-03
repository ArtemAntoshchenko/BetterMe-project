import pytest
from datetime import date, timedelta
from sqlalchemy import select
from tests.conftest import TrackingTestDAO, UserTestDAO, HabitCompletionTest, HabitTest, HabitTestDAO, AchievementTestDAO, UserAchievementsTestDAO, AchievementTest

class TestUserHabitIntegration:
    """Интеграционные тесты для связки User→Habit→Tracking"""

    async def test_habit_deletion_cascades_to_completions(self, db_session):
        """Проверяет каскадное удаление: при удалении привычки удаляются его выполнения"""
        user=await UserTestDAO.add(
            session=db_session,
            nickname="integration_user",
            login="integration_login",
            password="pass",
            email="integration@test.com",
            phone_number="+1234567890",
            first_name="Integration",
            last_name="Test",
            city="Test City",
            date_of_birth=date(1990, 1, 1)
        )
        habit=await HabitTestDAO.add(
            session=db_session,
            user_id=user.id,
            name="Integration Habit",
            description="Test habit for integration",
            complit=False,
            complit_today=False,
            goal=100,
            progress=0,
            step=10
        )
        assert user.id is not None
        assert habit.id is not None
        assert habit.user_id==user.id
        completions=[]
        for i in range(3):
            completion=await TrackingTestDAO.create_completion(session=db_session, habit_id=habit.id, user_id=user.id)
            completion.completed_date=date.today()-timedelta(days=1)
            await db_session.flush()
            completions.append(completion)
        query=select(HabitCompletionTest).where(HabitCompletionTest.habit_id==habit.id)
        result=(await db_session.scalars(query)).all()
        assert len(result)==3
        await HabitTestDAO.delete(session=db_session, id=habit.id)
        habit_check=await db_session.get(HabitTest, habit.id)
        assert habit_check is None
        completion_check=await db_session.get(HabitCompletionTest, completions[0].id)
        assert completion_check is None


    """Интеграционные тесты для связки Habit→Tracking→Achievement"""
    async def test_habit_achievement_flow(self, db_session):
        """Интеграционный тест полного цикла: привычка→выполнение→достижение"""
        user=await UserTestDAO.add(
            session=db_session,
            nickname="integration_user",
            login="integration_login",
            password="pass",
            email="integration@test.com",
            phone_number="+1234567890",
            first_name="Integration",
            last_name="Test",
            city="Test City",
            date_of_birth=date(1990, 1, 1)
        )
        habit=await HabitTestDAO.add(
            session=db_session,
            user_id=user.id,
            name="Integration Habit",
            description="Test habit for integration",
            complit=False,
            complit_today=False,
            goal=100,
            progress=0,
            step=10
        )
        achievement=await AchievementTestDAO.add(
            session=db_session,
            name="7 Day Streak",
            description="Complete habit for 7 days in a row",
            type="streak",
            goal=7
        )
        for i in range(7):
            completions=[]
            completion=await TrackingTestDAO.create_completion(session=db_session, habit_id=habit.id, user_id=user.id, completed_date=date.today()-timedelta(days=6-i))
            completions.append(completion)
            if completion.current_streak>=achievement.goal:
                await UserAchievementsTestDAO.add(session=db_session, user_id=user.id, achievement_id=achievement.id)
        last_completion=completions[-1]
        assert last_completion.current_streak==7
        user_achievements=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=user.id)
        achievement_ids=[ua.achievement_id for ua in user_achievements]
        assert achievement.id in achievement_ids
    

    """Интеграционные тесты для связки User→Achievement"""
    async def test_user_deletion_cascades_to_achievements(self, db_session):
        """Проверяет каскадное удаление: при удалении пользователя удаляются его достижения"""
        user=await UserTestDAO.add(
            session=db_session,
            nickname="integration_user",
            login="integration_login",
            password="pass",
            email="integration@test.com",
            phone_number="+1234567890",
            first_name="Integration",
            last_name="Test",
            city="Test City",
            date_of_birth=date(1990, 1, 1)
        )
        achievement1=await AchievementTestDAO.add(
            session=db_session,
            name="sample1",
            description="sample1",
            type="sampleType1",
            goal=10
        )
        achievement2=await AchievementTestDAO.add(
            session=db_session,
            name="sample2",
            description="sample2",
            type="sampleType2",
            goal=10
        )
        await UserAchievementsTestDAO.add(session=db_session, user_id=user.id, achievement_id=achievement1.id)
        await UserAchievementsTestDAO.add(session=db_session, user_id=user.id, achievement_id=achievement2.id)
        user_achievements_before=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=user.id)
        assert len(user_achievements_before)==2
        await UserTestDAO.delete(session=db_session, id=user.id)
        user_achievements_after=await UserAchievementsTestDAO.find_user_all(session=db_session, user_id=user.id)
        assert len(user_achievements_after)==0
        achievement_check1=await db_session.get(AchievementTest, achievement1.id)
        assert achievement_check1 is not None
        achievement_check2=await db_session.get(AchievementTest, achievement2.id)
        assert achievement_check2 is not None
