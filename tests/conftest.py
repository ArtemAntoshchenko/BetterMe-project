import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from datetime import datetime
from typing import Annotated
from datetime import date
from typing import List, AsyncGenerator, Dict, Any
from backend.DAO.dao_habits import HabitDAO
from backend.DAO.dao_achievement import AchievementDAO
from backend.DAO.dao_registration import UserDAO
from backend.DAO.dao_user_achievements import UserAchievementsDAO
from backend.DAO.dao_tracking import TrackingDAO
from backend.db.database import get_db
from contextlib import asynccontextmanager
from sqlalchemy import func
import os
import tempfile
from httpx import AsyncClient


TEST_TYPE = os.getenv("TEST_TYPE", "integration")

def get_test_db_url():
    if TEST_TYPE == "e2e":
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        return f"sqlite+aiosqlite:///{temp_db.name}"
    else:
        return "sqlite+aiosqlite:///:memory:"

_engine = None
_sessionmaker = None
_test_db_file = None

def get_engine():
    """Создаёт движок один раз с учётом типа тестов"""
    global _engine, _sessionmaker, _test_db_file
    if _engine is None:
        db_url=get_test_db_url()
        if db_url.startswith("sqlite+aiosqlite:///") and db_url != "sqlite+aiosqlite:///:memory:":
            _test_db_file = db_url.replace("sqlite+aiosqlite:///", "")
        _engine = create_async_engine(db_url, echo=False)
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

class UserAchievementsTestDAO(UserAchievementsDAO):
    model=UserAchievementsTest

class HabitTestDAO(HabitDAO):
    model=HabitTest

class TrackingTestDAO(TrackingDAO):
    model=HabitCompletionTest

    @classmethod
    async def get_all_habits_heatmap_data(cls, session: AsyncSession, user_id: int, days: int=90)-> List[dict]:
        if session:
            habits=await HabitTestDAO.find_all_active(session=session, profile_id=user_id)
            result=[]
            for habit in habits:
                heatmap_data=await cls.get_heatmap_data(habit.id, days, session=session)
                stats=await cls.get_heatmap_stats(habit.id, days, session=session)
                hue=(habit.id * 137)%360
                result.append({
                    'habit_id': habit.id,
                    'habit_name': habit.name,
                    'color': f"hsl({hue}, 70%, 50%)",
                    'heatmap_data': heatmap_data,
                    'current_streak': stats['current_streak'],
                    'total_completions': stats['total_completions']
                })
            return result
        else:
            async with get_db() as new_session:
                habits=await HabitTestDAO.find_all_active(session=new_session, profile_id=user_id)
                result=[]
                for habit in habits:
                    heatmap_data=await cls.get_heatmap_data(habit.id, days, session=new_session)
                    stats=await cls.get_heatmap_stats(habit.id, days, session=new_session)
                    hue=(habit.id * 137)%360
                    result.append({
                        'habit_id': habit.id,
                        'habit_name': habit.name,
                        'color': f"hsl({hue}, 70%, 50%)",
                        'heatmap_data': heatmap_data,
                        'current_streak': stats['current_streak'],
                        'total_completions': stats['total_completions']
                    })
                return result


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Автоматически создаёт и чистит таблицы для каждого теста"""
    engine, _ = get_engine()
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseTest.metadata.create_all)
    
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseTest.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session():
    """Возвращает сессию для тестов"""
    global TEST_TYPE
    old_type = TEST_TYPE
    os.environ["TEST_TYPE"] = "integration"
    _, sessionmaker = get_engine()
    async with sessionmaker() as session:
        async with session.begin():
            yield session
    os.environ["TEST_TYPE"] = old_type


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
        nickname="users",
        login="logins",
        password="passs",
        email="users@test.com",
        phone_number="+1222222221",
        first_name="Firsts",
        last_name="Lasts",
        city="Citys",
        date_of_birth=date(1991, 1, 1)
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


@pytest.fixture(scope="function")
async def sample_user_achievement(db_session):
    """Создаёт пользователя"""
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
    """Создаёт тестовое достижение"""
    achievement=await AchievementTestDAO.add(
        session=db_session,
        name="sample",
        description="sample",
        type="sampleType",
        goal=10
    )
    """Создаёт связь между пользователем и достижением"""
    userAchievements=await UserAchievementsTestDAO.add(
        session=db_session,
        user_id=user.id,
        achievement_id=achievement.id
    )
    return achievement, user


@pytest.fixture(scope='function', autouse=True)
def switch_to_test_models():
    """Временно подменяет модели в оригинальных DAO на тестовые"""
    if os.environ.get('E2E_TESTING') == 'true':
        from backend.DAO.dao_habits import HabitDAO

        # Сохраняем оригинальные модели
        original_habit_model = HabitDAO.model

        # Подменяем на тестовые
        HabitDAO.model = HabitTest
        yield
        
        # Восстанавливаем
        HabitDAO.model = original_habit_model
    else:
        yield

@pytest.fixture(scope='function')
async def live_server():
    """Запускает реальное FastAPI приложение для E2E тестов"""
    import uvicorn
    from backend.main import app
    import httpx
    
    app.state.testing = True
    app.state.e2e_testing = True
    os.environ['TESTING'] = 'true'
    os.environ['E2E_TESTING'] = 'true'
    os.environ['TEST_DB_URL'] = get_test_db_url()
    
    config = uvicorn.Config(app, host='127.0.0.1', port=8888, log_level='error', loop='asyncio')
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())
    
    # Увеличиваем время ожидания запуска сервера
    await asyncio.sleep(3)
    
    # Проверяем, что сервер действительно запустился
    async with httpx.AsyncClient() as client:
        for i in range(15):  # Увеличил количество попыток
            try:
                await client.get("http://127.0.0.1:8888")
                break
            except:
                await asyncio.sleep(1)
        else:
            raise RuntimeError("Сервер не запустился после 15 попыток")
    
    yield "http://127.0.0.1:8888"
    
    server.should_exit = True
    await task
    
    if _test_db_file and os.path.exists(_test_db_file):
        try:
            os.unlink(_test_db_file)
        except:
            pass

@pytest.fixture(scope="function")
async def e2e_client(live_server):
    """HTTP клиент для прямых API вызовов в E2E тестах"""
    # Добавляем небольшую задержку перед созданием клиента
    await asyncio.sleep(0.5)
    async with AsyncClient(base_url=live_server, timeout=30.0) as client:  # Увеличил таймаут
        yield client

@pytest.fixture(scope="function")
async def authenticated_user_e2e(e2e_client, live_server):
    """Создаёт авторизованного пользователя через API для E2E тестов"""
    import time
    
    # Небольшая задержка
    await asyncio.sleep(0.5)
    
    timestamp = int(time.time())
    short_timestamp = str(timestamp)[-5:]
    
    user_data = {
        "nickname": f"e2e_user_{short_timestamp}",
        "login": f"e2e_login_{short_timestamp}",
        "password": "TestPass123",
        "email": f"e2e_{short_timestamp}@test.com",
        "phone_number": f"+7{short_timestamp}12345",
        "first_name": "E2E",
        "last_name": "User",
        "city": "Test City",
        "date_of_birth": "1990-01-01"
    }
    
    # Регистрация через API
    response = await e2e_client.post("/auth/registration", json=user_data)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    
    # Вход через API
    response = await e2e_client.post("/auth/login", json={
        "login": user_data["login"],
        "password": user_data["password"]
    })
    assert response.status_code == 200, f"Login failed: {response.text}"
    
    token = response.json()['access_token']
    user_data['token'] = token
    return user_data

@pytest.fixture(scope="function")
async def browser_context():
    """Создаёт контекст браузера для E2E тестов"""
    from playwright.async_api import async_playwright
    playwright=await async_playwright().start()
    headless=os.getenv('HEADLESS', 'true').lower()=='true'
    browser=await playwright.chromium.launch(
        headless=headless,
        args=['--disable-dev-shm-usage']
    )
    context=await browser.new_context(
        viewport={'width':1920, 'height':1080},
        locale='ru-Ru'
    )
    yield context
    await context.close()
    await browser.close()
    await playwright.stop()

@pytest.fixture
async def page(browser_context):
    """Создаёт новую страницу для E2E тестов"""
    page=await browser_context.new_page()
    try:
        yield page
    except:
        screenshot=await page.screenshot()
        with open(f'e2e_error_{asyncio.get_event_loop().time()}.png", "wb"') as f:
            f.write(screenshot)
        raise

@pytest.fixture
async def e2e_habit(e2e_client, authenticated_user_e2e):
    """Создаёт привычку через API для E2E тестов"""
    import time
    e2e_client.cookies.set('users_access_token', authenticated_user_e2e['token'])
    habit_data={
        "name":f"E2E Habit {int(time.time())}",
        "description":"Test habit for E2E",
        "goal":100,
        "step":10
    }
    response=await e2e_client.post('/habits/main/createNewHabit', json=habit_data)
    assert response.status_code==200
    return {**habit_data, 'id':None}

@pytest.fixture(scope="function", autouse=True)
def cleanup_e2e_files():
    """Очищает временные файлы после всех тестов"""
    yield
    global _test_db_file
    if _test_db_file and os.path.exists(_test_db_file):
        try:
            os.unlink(_test_db_file)
        except:
            pass
