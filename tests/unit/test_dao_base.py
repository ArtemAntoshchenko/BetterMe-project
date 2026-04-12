import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from tests.conftest import UserTestDAO, HabitTestDAO

class TestBaseDAO:

    async def test_find_all_returns_all_records(self, db_session, two_users):
        """BaseDAO.find_all(): должен возвращать все записи"""
        user1, user2 = two_users
        
        all_users = await UserTestDAO.find_all(session=db_session)
        
        assert len(all_users) == 2
        user_ids = [u.id for u in all_users]
        assert user1.id in user_ids
        assert user2.id in user_ids
    
    async def test_find_all_empty_table(self, db_session):
        """BaseDAO.find_all(): пустая таблица возвращает пустой список"""
        
        result = await UserTestDAO.find_all(session=db_session)
        
        assert result == []
        assert isinstance(result, list)
    
    async def test_find_all_returns_correct_type(self, db_session, sample_user):
        """BaseDAO.find_all(): возвращает список моделей"""
        result = await UserTestDAO.find_all(session=db_session)
        
        assert isinstance(result, list)
        assert all(isinstance(item, type(sample_user)) for item in result)
    
    async def test_find_one_or_none_exists(self, db_session, sample_user):
        """BaseDAO.find_one_or_none(): находит существующую запись"""
        found = await UserTestDAO.find_one_or_none(
            session=db_session,
            id=sample_user.id
        )
        
        assert found is not None
        assert found.id == sample_user.id
        assert found.nickname == sample_user.nickname
    
    async def test_find_one_or_none_not_exists(self, db_session):
        """BaseDAO.find_one_or_none(): несуществующая запись возвращает None"""
        found = await UserTestDAO.find_one_or_none(session=db_session, id=99999)
        
        assert found is None
    
    async def test_find_one_or_none_with_multiple_filters(self, db_session):
        """BaseDAO.find_one_or_none(): фильтрация по нескольким полям"""
        user1 = await UserTestDAO.add(
            session=db_session,
            nickname="john_doe",
            login="john1",
            password="pass",
            email="john1@test.com",
            phone_number="+1111111111",
            first_name="John",
            last_name="Doe",
            city="City",
            date_of_birth=date(1990, 1, 1)
        )
        
        user2 = await UserTestDAO.add(
            session=db_session,
            nickname="john_smith",
            login="john2",
            password="pass",
            email="john2@test.com",
            phone_number="+2222222222",
            first_name="John",
            last_name="Smith",
            city="City",
            date_of_birth=date(1990, 1, 1)
        )
        
        found = await UserTestDAO.find_one_or_none(
            session=db_session,
            nickname="john_smith",
            email="john2@test.com"
        )
        
        assert found is not None
        assert found.last_name == "Smith"
    
    async def test_add_creates_record(self, db_session):
        """BaseDAO.add(): создаёт запись в БД"""
        user = await UserTestDAO.add(
            session=db_session,
            nickname="new_user",
            login="newlogin",
            password="hashed_pass",
            email="new@test.com",
            phone_number="+9999999999",
            first_name="New",
            last_name="User",
            city="New City",
            date_of_birth=date(1995, 5, 5)
        )
        
        assert user.id is not None
        assert user.nickname == "new_user"
        
        saved = await UserTestDAO.find_one_or_none(session=db_session, id=user.id)
        assert saved is not None
        assert saved.nickname == "new_user"
    
    async def test_add_with_duplicate_unique_field(self, db_session, sample_user):
        """BaseDAO.add(): дубликат unique поля вызывает ошибку"""
        with pytest.raises(IntegrityError):
            await UserTestDAO.add(
                session=db_session,
                nickname=sample_user.nickname,
                login="another_login",
                password="pass",
                email="another@test.com",
                phone_number="+7777777777",
                first_name="Another",
                last_name="User",
                city="City",
                date_of_birth=date(1990, 1, 1)
            )
    
    async def test_update_single_field(self, db_session, sample_user):
        """BaseDAO.update(): обновление одного поля"""
        updated = await UserTestDAO.update(
            session=db_session,
            filter_by={"id": sample_user.id},
            nickname="new_name"
        )
        
        assert updated is not None
        assert updated.nickname == "new_name"
        assert updated.id == sample_user.id
    
    async def test_update_multiple_fields(self, db_session, sample_user):
        """BaseDAO.update(): обновление нескольких полей"""
        updated = await UserTestDAO.update(
            session=db_session,
            filter_by={"id": sample_user.id},
            nickname="new_nick",
            city="New City",
            email="new@test.com"
        )
        
        assert updated.nickname == "new_nick"
        assert updated.city == "New City"
        assert updated.email == "new@test.com"
    
    async def test_update_nonexistent_record(self, db_session):
        """BaseDAO.update(): обновление несуществующей записи возвращает None"""
        result = await UserTestDAO.update(
            session=db_session,
            filter_by={"id": 99999},
            nickname="anything"
        )
        
        assert result is None
    
    async def test_delete_single_record(self, db_session, sample_user):
        """BaseDAO.delete(): удаление одной записи"""
        deleted_count = await UserTestDAO.delete(
            session=db_session,
            id=sample_user.id
        )
        
        assert deleted_count == 1
        
        found = await UserTestDAO.find_one_or_none(session=db_session, id=sample_user.id)
        assert found is None
    
    async def test_delete_multiple_records(self, db_session):
        """BaseDAO.delete(): удаление нескольких записей"""
        await UserTestDAO.add(
            session=db_session,
            nickname="user1",
            login="login1",
            password="pass",
            email="user1@test.com",
            phone_number="+1111111111",
            first_name="User",
            last_name="One",
            city="Moscow",
            date_of_birth=date(1990, 1, 1)
        )
        
        await UserTestDAO.add(
            session=db_session,
            nickname="user2",
            login="login2",
            password="pass",
            email="user2@test.com",
            phone_number="+2222222222",
            first_name="User",
            last_name="Two",
            city="Moscow",
            date_of_birth=date(1990, 1, 1)
        )
        
        deleted_count = await UserTestDAO.delete(session=db_session, city="Moscow")
        
        assert deleted_count == 2
        
        remaining = await UserTestDAO.find_all(session=db_session)
        assert len(remaining) == 0
    
    async def test_delete_without_filters_raises_error(self, db_session):
        """BaseDAO.delete(): без фильтров вызывает ошибку"""
        with pytest.raises(ValueError, match="Необходимо указать хотя бы один параметр"):
            await UserTestDAO.delete(session=db_session)  
    
    async def test_delete_all_with_flag(self, db_session):
        """BaseDAO.delete(): delete_all=True удаляет все записи"""
        await UserTestDAO.add(
            session=db_session,
            nickname="user1",
            login="login1",
            password="pass",
            email="user1@test.com",
            phone_number="+1111111111",
            first_name="User",
            last_name="One",
            city="City",
            date_of_birth=date(1990, 1, 1)
        )
        
        await UserTestDAO.add(
            session=db_session,
            nickname="user2",
            login="login2",
            password="pass",
            email="user2@test.com",
            phone_number="+2222222222",
            first_name="User",
            last_name="Two",
            city="City",
            date_of_birth=date(1990, 1, 1)
        )
        
        deleted_count = await UserTestDAO.delete(session=db_session, delete_all=True)
        
        assert deleted_count == 2
        
        all_users = await UserTestDAO.find_all(session=db_session)
        assert len(all_users) == 0
    
    async def test_full_crud_cycle(self, db_session):
        """BaseDAO: полный цикл CRUD"""
        user = await UserTestDAO.add(
            session=db_session,
            nickname="crud_user",
            login="crud",
            password="pass",
            email="crud@test.com",
            phone_number="+3333333333",
            first_name="CRUD",
            last_name="User",
            city="Test City",
            date_of_birth=date(1990, 1, 1)
        )
        assert user.id is not None
        
        found = await UserTestDAO.find_one_or_none(session=db_session, id=user.id)
        assert found is not None
        
        updated = await UserTestDAO.update(
            session=db_session,
            filter_by={"id": user.id},
            city="Updated City"
        )
        assert updated.city == "Updated City"
        
        deleted = await UserTestDAO.delete(session=db_session, id=user.id)
        assert deleted == 1
        
        not_found = await UserTestDAO.find_one_or_none(session=db_session, id=user.id)
        assert not_found is None
    
    async def test_work_with_different_models(self, db_session, sample_user):
        """BaseDAO: работает с разными моделями"""
        user = await UserTestDAO.find_one_or_none(session=db_session, id=sample_user.id)
        assert user is not None
        
        habit = await HabitTestDAO.add(
            session=db_session,
            user_id=sample_user.id,
            name="Test Habit",
            description="Test",
            complit=False,
            complit_today=False,
            goal=10,
            step=1
        )
        assert habit.id is not None
        
        habits = await HabitTestDAO.find_all(session=db_session)
        assert len(habits) == 1