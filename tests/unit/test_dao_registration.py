import pytest
from datetime import date
from tests.conftest import UserTestDAO


class TestUserDAO:

    async def test_change_user_status_correct_change_status(self, db_session):
        """UserDAO.changeUserStatus(): должен правильно менять статус суперпользователя"""
        user=await UserTestDAO.add(
            session=db_session,
            nickname="sample",
            login="sample",
            password="pass",
            email="sample@test.com",
            phone_number="+1234567890",
            first_name="Sample",
            last_name="User",
            city="Sample City",
            date_of_birth=date(1990, 1, 1),
            super_user=False
        )
        result=await UserTestDAO.changeUserStatus(session=db_session, user_id=user.id)
        assert user.super_user==True

    async def test_change_user_status_nonexistent_user(self, db_session):
        """UserDAO.changeUserStatus(): при запросе несуществующего пользователя возвращает None"""
        result=await UserTestDAO.changeUserStatus(session=db_session, user_id=99)
        assert result is None


    async def test_find_superuser_return_all_superusers(self, db_session):
        """UserDAO.find_superusers(): должен вернуть всех суперпользователей"""
        user1=await UserTestDAO.add(
            session=db_session,
            nickname="sample",
            login="sample",
            password="pass",
            email="sample@test.com",
            phone_number="+1234567890",
            first_name="Sample",
            last_name="User",
            city="Sample City",
            date_of_birth=date(1990, 1, 1),
            super_user=True
        )
        user2=await UserTestDAO.add(
            session=db_session,
            nickname="sample2",
            login="sample2",
            password="pass2",
            email="sample@test.com2",
            phone_number="+12345678901",
            first_name="Sample2",
            last_name="User2",
            city="Sample City2",
            date_of_birth=date(1990, 1, 2),
            super_user=False
        )
        result=await UserTestDAO.find_superusers(session=db_session)
        assert user1.id in [u.id for u in result]
        assert user2.id not in [u.id for u in result]

    async def test_find_superuser_returns_correct_type(self, db_session,  sample_user):
        """UserDAO.find_superusers(): возвращает список моделей"""
        user1=await UserTestDAO.add(
            session=db_session,
            nickname="sample1",
            login="sample1",
            password="pass1",
            email="sample@test.com1",
            phone_number="+12345678903",
            first_name="Sample1",
            last_name="User1",
            city="Sample City1",
            date_of_birth=date(1990, 1, 3),
            super_user=True
        )
        user2=await UserTestDAO.add(
            session=db_session,
            nickname="sample2",
            login="sample2",
            password="pass2",
            email="sample@test.com2",
            phone_number="+12345678901",
            first_name="Sample2",
            last_name="User2",
            city="Sample City2",
            date_of_birth=date(1990, 1, 2),
            super_user=False
        )
        result=await UserTestDAO.find_superusers(session=db_session)
        assert isinstance(result, list)
        assert all(isinstance(i, type(sample_user)) for i in result)

    async def test_find_superuser_with_nonexistent_superusers(self, db_session):
        """UserDAO.find_superusers(): при отсутсвии суперпользователей, возвращает пустой список"""
        user=await UserTestDAO.add(
            session=db_session,
            nickname="sample",
            login="sample",
            password="pass",
            email="sample@test.com",
            phone_number="+1234567890",
            first_name="Sample",
            last_name="User",
            city="Sample City",
            date_of_birth=date(1990, 1, 1),
            super_user=False
        )
        result=await UserTestDAO.find_superusers(session=db_session)
        assert isinstance(result, list)
        assert result==[]
        