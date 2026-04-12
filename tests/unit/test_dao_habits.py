import pytest
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from tests.conftest import UserTestDAO, HabitTestDAO

class TestHabitsDAO:

    async def test_find_all_return_all(self, db_session, two_habits):
        """HabitsDAO.find_all(): должен возвращать все записи"""
        habit1, habit2=two_habits
        all_habits=await HabitTestDAO.find_all(session=db_session, profile_id=habit1.user_id)
        assert habit1.id!=habit2.id
        assert len(all_habits)==2
        habits_id=[h.id for h in all_habits]
        assert habit1.id in habits_id
        assert habit2.id in habits_id

    async def test_find_all_empty_table(self, db_session):
        """HabitsDAO.find_all(): пустая таблица возвращает пустой список"""
        result=await HabitTestDAO.find_all(session=db_session)
        assert isinstance(result, list)
        assert result==[]

    async def test_find_all_returns_correct_type(self, db_session, two_habits, sample_habit):
        """HabitsDAO.find_all(): возвращает список моделей"""
        habit1, habit2=two_habits
        result=await HabitTestDAO.find_all(session=db_session, profile_id=habit1.user_id)
        assert isinstance(result, list)
        assert all(isinstance(i, type(sample_habit)) for i in result)

    async def test_find_all_active_return_all(self, db_session):
        """HabitsDAO.find_all_active(): должен возвращать все активные записи"""
        user=await UserTestDAO.add(
            session=db_session,
            nickname="user",
            login="login",
            password="pass",
            email="user@test.com",
            phone_number="+2222222222",
            first_name="First",
            last_name="Last",
            city="City",
            date_of_birth=date(1990, 1, 1)
        )
        user_id=user.id
        habit1=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id,
            name="sample1",
            description="sample1",
            complit=False,
            complit_today=True,
            goal=100,
            progress=20,
            step=10
        )
        habit2=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id,
            name="sample2",
            description="sample2",
            complit=True, 
            complit_today=True,
            goal=110,
            progress=30,
            step=5
        )

        result=await HabitTestDAO.find_all_active(session=db_session, profile_id=habit1.user_id)
        assert len(result)==1
        habits_id=[h.id for h in result]
        assert habit1.id in habits_id
        assert habit2.id not in habits_id


