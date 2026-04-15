import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from datetime import datetime
from typing import Annotated
from datetime import date
from typing import List
from backend.DAO.dao_base import BaseDAO
from backend.DAO.dao_habits import HabitDAO
from backend.DAO.dao_achievement import AchievementDAO
from backend.DAO.dao_registration import UserDAO
from backend.db.database import get_db
from contextlib import asynccontextmanager
from sqlalchemy import func


_engine = None
_sessionmaker = None

def get_engine():
    """Создаёт движок один раз"""
    global _engine, _sessionmaker
    if _engine is None:
        _engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
        _sessionmaker = sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
    return _engine, _sessionmaker

created_at=Annotated[datetime, mapped_column(server_default=func.now())]
updated_at=Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
int_pk=Annotated[int, mapped_column(primary_key=True)]
str_uniq=Annotated[str, mapped_column(unique=True, nullable=False)]
int_null_true=Annotated[int, mapped_column(nullable=True)]
bool_False=Annotated[bool, mapped_column(default=False)]

class BaseTest(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class UserTest(BaseTest):
    __tablename__ = 'test_users'

    id: Mapped[int_pk]
    nickname: Mapped[str_uniq]
    login: Mapped[str_uniq]
    password: Mapped[str]
    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    city: Mapped[str]
    date_of_birth: Mapped[date]
    premium: Mapped[bool]=mapped_column(default=False)
    super_user: Mapped[bool]=mapped_column(default=False)
    achievements: Mapped[List['UserAchievementsTest']]=relationship(back_populates='user', cascade='all, delete-orphan')

class AchievementTest(BaseTest):
    __tablename__ = 'test_achievements'

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str]=mapped_column(Text)
    type: Mapped[str]=mapped_column(String(50), nullable=True)
    goal: Mapped[int]=mapped_column(default=0)
    users: Mapped[List['UserAchievementsTest']]=relationship(back_populates='achievement', cascade='all, delete-orphan')

class UserAchievementsTest(BaseTest):
    __tablename__ = 'test_user_achievements'

    id: Mapped[int_pk]
    user_id: Mapped[int]=mapped_column(ForeignKey('test_users.id', ondelete='CASCADE'))
    achievement_id: Mapped[int]=mapped_column(ForeignKey('test_achievements.id', ondelete='CASCADE'))
    user: Mapped[UserTest]=relationship(back_populates='achievements')
    achievement: Mapped[AchievementTest]=relationship(back_populates='users')

    __table_args__ = (
        UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement'),
    )

class HabitTest(BaseTest):
    __tablename__ = 'test_habits'

    id: Mapped[int_pk]
    user_id: Mapped[int]=mapped_column(ForeignKey('test_users.id', ondelete='CASCADE'))
    name: Mapped[str_uniq]
    description: Mapped[str]=mapped_column(Text)
    complit: Mapped[bool_False]
    complit_today: Mapped[bool_False]
    goal: Mapped[int_null_true]
    progress: Mapped[int]=mapped_column(default=0)
    step: Mapped[int_null_true]
    completions: Mapped[List['HabitCompletionTest']]=relationship(back_populates='habit', cascade='all, delete-orphan')

    @property
    def has_completions(self)-> bool:
        return len(self.completions)>0

class HabitCompletionTest(BaseTest):
    __tablename__ = 'test_habit_completions'

    id: Mapped[int_pk]
    habit_id: Mapped[int]=mapped_column(ForeignKey('test_habits.id', ondelete='CASCADE'))
    user_id: Mapped[int]=mapped_column(ForeignKey('test_users.id', ondelete='CASCADE'))
    completed_date: Mapped[date]=mapped_column(default=date.today)
    completed_at: Mapped[datetime]=mapped_column(default=datetime.now)
    current_streak: Mapped[int]=mapped_column(default=0)
    longest_streak: Mapped[int]=mapped_column(default=0)
    habit: Mapped[HabitTest]=relationship(back_populates='completions')


class AchievementTestDAO(AchievementDAO):
    model=AchievementTest

class UserTestDAO(UserDAO):
    model=UserTest

class UserAchievementsTestDAO(BaseDAO):
    model=UserAchievementsTest

class HabitTestDAO(HabitDAO):
    model=HabitTest

class TrackingTestDAO(BaseDAO):
    model=HabitCompletionTest


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Автоматически создаёт и чистит таблицы для каждого теста"""
    engine, _ = get_engine()
    
    # Создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(BaseTest.metadata.create_all)
    
    yield
    
    # Чистим таблицы после теста
    async with engine.begin() as conn:
        await conn.run_sync(BaseTest.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session():
    """Возвращает сессию для тестов"""
    _, sessionmaker = get_engine()
    async with sessionmaker() as session:
        async with session.begin():
            yield session


@pytest.fixture(scope="function")
async def sample_user(db_session):
    """Создаёт тестового пользователя"""
    user = await UserTestDAO.add(
        session=db_session,
        nickname="sample",
        login="sample",
        password="pass",
        email="sample@test.com",
        phone_number="+1234567890",
        first_name="Sample",
        last_name="User",
        city="Sample City",
        date_of_birth=date(1990, 1, 1)
    )
    return user


@pytest.fixture(scope="function")
async def two_users(db_session):
    """Создаёт двух тестовых пользователей"""
    user1 = await UserTestDAO.add(
        session=db_session,
        nickname="user_a",
        login="login_a",
        password="pass",
        email="user_a@test.com",
        phone_number="+1111111111",
        first_name="First A",
        last_name="Last A",
        city="City A",
        date_of_birth=date(1990, 1, 1)
    )
    
    user2 = await UserTestDAO.add(
        session=db_session,
        nickname="user_b",
        login="login_b",
        password="pass",
        email="user_b@test.com",
        phone_number="+2222222222",
        first_name="First B",
        last_name="Last B",
        city="City B",
        date_of_birth=date(1990, 1, 1)
    )
    
    return user1, user2 

@pytest.fixture(scope="function")
async def sample_habit(db_session):
    """Создаёт user для тестовой привычки"""
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
    """Создаёт тестовую привычку"""
    habit=await HabitTestDAO.add(
        session=db_session,
        user_id=user_id,
        name="sample",
        description="sample",
        complit=False,
        complit_today=False,
        goal=100,
        progress=20,
        step=10
    )
    return habit


@pytest.fixture(scope="function")
async def two_habits(db_session):
    """Создаёт user для тестовых привычек"""
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

    """Создаёт две тестовые привычки"""
    habit1=await HabitTestDAO.add(
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
    
    habit2=await HabitTestDAO.add(
        session=db_session,
        user_id=user_id,
        name="sample2",
        description="sample2",
        complit=False,
        complit_today=False,
        goal=110,
        progress=30,
        step=5
    )
    return habit1, habit2 