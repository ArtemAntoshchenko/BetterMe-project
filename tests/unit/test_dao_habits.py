import pytest
from datetime import date, datetime, timedelta
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

    async def test_find_all_returns_habits_for_correct_user(self, db_session):
        """HabitsDAO.find_all(): возвращает активные привычки только указанного пользователя"""
        user1=await UserTestDAO.add(
            session=db_session,
            nickname="user1",
            login="login1",
            password="pass1",
            email="user@test.com1",
            phone_number="+22222222221",
            first_name="First1",
            last_name="Last1",
            city="City1",
            date_of_birth=date(1990, 1, 1)
        )
        user2=await UserTestDAO.add(
            session=db_session,
            nickname="user2",
            login="login2",
            password="pass2",
            email="user@test.com2",
            phone_number="+22222222222",
            first_name="First2",
            last_name="Last2",
            city="City2",
            date_of_birth=date(1990, 1, 2)
        )
        user_id1=user1.id
        habit1=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id1,
            name="sample1",
            description="sample1",
            complit=False,
            complit_today=True,
            goal=100,
            progress=20,
            step=10
        )
        user_id2=user2.id
        habit2=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id2,
            name="sample2",
            description="sample2",
            complit=True, 
            complit_today=True,
            goal=110,
            progress=30,
            step=5
        )
        result=await HabitTestDAO.find_all(session=db_session, profile_id=user1.id)
        assert len(result)==1
        assert habit1.id in [h.id for h in result]
        assert habit2.id not in [h.id for h in result]

    async def test_find_all_with_nonexistent_user(self, db_session):
        """HabitsDAO.find_all(): при запросе несуществующего пользователя возвращает пустой список"""
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
        habit=await HabitTestDAO.add(
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
        result=await HabitTestDAO.find_all(session=db_session, profile_id=99)
        assert isinstance(result, list)
        assert result==[]

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

    async def test_find_all_active_empty_table(self, db_session):
        """HabitsDAO.find_all_active(): пустая таблица возвращает пустой список"""
        result=await HabitTestDAO.find_all_active(session=db_session)
        assert result==[]
        assert isinstance(result, list)
    
    async def test_find_all_active_correct_type(self, db_session, two_habits, sample_habit):
        """HabitsDAO.find_all_active(): возвращает список моделей"""
        habit1, habit2=two_habits
        result=await HabitTestDAO.find_all_active(session=db_session, profile_id=habit1.user_id)
        assert isinstance(result, list)
        assert all(isinstance(i, type(sample_habit)) for i in result)

    async def test_find_all_active_returns_habits_for_correct_user(self, db_session):
        """HabitsDAO.find_all_active(): возвращает активные привычки только указанного пользователя"""
        user1=await UserTestDAO.add(
            session=db_session,
            nickname="user1",
            login="login1",
            password="pass1",
            email="user@test.com1",
            phone_number="+22222222221",
            first_name="First1",
            last_name="Last1",
            city="City1",
            date_of_birth=date(1990, 1, 1)
        )
        user2=await UserTestDAO.add(
            session=db_session,
            nickname="user2",
            login="login2",
            password="pass2",
            email="user@test.com2",
            phone_number="+22222222222",
            first_name="First2",
            last_name="Last2",
            city="City2",
            date_of_birth=date(1990, 1, 2)
        )
        user_id1=user1.id
        habit1=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id1,
            name="sample1",
            description="sample1",
            complit=False,
            complit_today=True,
            goal=100,
            progress=20,
            step=10
        )
        user_id2=user2.id
        habit2=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id2,
            name="sample2",
            description="sample2",
            complit=True, 
            complit_today=True,
            goal=110,
            progress=30,
            step=5
        )
        result=await HabitTestDAO.find_all_active(session=db_session, profile_id=user1.id)
        assert len(result)==1
        assert habit1.id in [h.id for h in result]
        assert habit2.id not in [h.id for h in result]

    async def test_find_all_active_with_nonexistent_user(self, db_session):
        """HabitsDAO.find_all_active(): при запросе несуществующего пользователя возвращает пустой список"""
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
        habit=await HabitTestDAO.add(
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
        result=await HabitTestDAO.find_all_active(session=db_session, profile_id=99)
        assert isinstance(result, list)
        assert result==[]


    async def test_complit_habit_change_status_correct(self, db_session):
        """HabitsDAO.complite_habit(): правильно меняет статус привычки"""
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
        habit=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id,
            name="sample1",
            description="sample1",
            complit=False,
            complit_today=False,
            goal=100,
            progress=20,
            step=10
        )
        result=await HabitTestDAO.complit_habit(session=db_session, habit_id=habit.id, user_id=user.id)
        await db_session.refresh(habit)
        assert habit.complit_today==True
        assert habit.progress==30
    

    async def test_daily_habit_status_update_change_status_correct(self, db_session):
        """HabitsDAO.daily_habit_status_update(): правильно меняет статус привычки"""
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
        old_date=datetime.now()-timedelta(days=2)
        habit=await HabitTestDAO.add(
            session=db_session,
            user_id=user_id,
            name="sample1",
            description="sample1",
            complit=False,
            complit_today=True,
            goal=100,
            progress=20,
            step=10,
            updated_at=old_date
        )
        result=await HabitTestDAO.daily_habit_status_update(session=db_session, habit_id=habit.id)
        await db_session.refresh(habit)
        assert habit.complit_today==False
        assert habit.updated_at==datetime.now()
        assert habit.updated_at>old_date
        assert result=='Статус привычек был обновлен'




