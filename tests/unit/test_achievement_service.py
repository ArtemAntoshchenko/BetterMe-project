import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from unittest.mock import AsyncMock, MagicMock, patch
from backend.core.achievement_service import AchievementTypes, AchievementService
from backend.db.models import User, Achievement, UserAchievements

class TestAchievementService:
    """Юнит-тесты с моками для AchievementService"""

    """Фикстуры"""
    @pytest.fixture
    def mock_user(self):
        """Создаёт мок пользователя"""
        user=MagicMock(spec=User)
        user.id=1
        user.nickname="test_user"
        user.login="test_login"
        user.password="password"
        user.email="test@test.com"
        user.phone_number="+1234567890"
        user.first_name="Test"
        user.last_name="User"
        user.city="Test City"
        user.date_of_birth=date(1990, 1, 1)
        return user
    @pytest.fixture
    def mock_achievement(self):
        """Создаёт мок достижения"""
        achievement=MagicMock(spec=Achievement)
        achievement.id=1
        achievement.name="Profile"
        achievement.type=AchievementTypes.PROFILE_FILLED
        achievement.goal=5
        achievement.description="Fill profile fields"
        return achievement
    @pytest.fixture
    def mock_achievement_streak(self):
        """Создаёт мок достижения для streak"""
        achievement=MagicMock(spec=Achievement)
        achievement.id=2
        achievement.name="Streak"
        achievement.type=AchievementTypes.LONGEST_STREAK
        achievement.goal=7
        achievement.description="7 days streak"
        return achievement


    """Тесты для check_profile_filled"""
    def test_check_profile_filled_all_fields_success(self, mock_user, mock_achievement):
        """Проверяет: профиль заполнен полностью - возвращает True"""
        mock_achievement.goal=9
        result=AchievementService._check_profile_filled(mock_user, mock_achievement)
        assert result is True

    def test_check_profile_filled_partial_fields(self, mock_user, mock_achievement):
        """Проверяет: профиль заполнен частично - возвращает False"""
        mock_achievement.goal=9
        mock_user.city=""
        result=AchievementService._check_profile_filled(mock_user, mock_achievement)
        assert result is False

    def test_check_profile_filled_empty_strings_count_as_empty(self, mock_user, mock_achievement):
        """Проверяет: пустые строки считаются незаполненными"""
        mock_achievement.goal=9
        mock_user.nickname="   "  
        result=AchievementService._check_profile_filled(mock_user, mock_achievement)
        assert result is False


    """Тесты для check_longest_streak"""
    @pytest.mark.asyncio
    async def test_check_longest_streak_success(self, mock_user, mock_achievement_streak):
        """Проверяет: стрик соответствует цели - достижение выдаётся"""
        mock_achievement_streak.goal=7
        with patch('backend.core.achievement_service.TrackingDAO') as mock_tracking:
            mock_tracking.get_user_longest_streak=AsyncMock(return_value=10)
            result=await AchievementService._check_longest_streak(mock_user, mock_achievement_streak)
            assert result is True
            mock_tracking.get_user_longest_streak.assert_called_once_with(user_id=mock_user.id)
    
    @pytest.mark.asyncio
    async def test_check_longest_streak_not_enough(self, mock_user, mock_achievement_streak):
        """Проверяет: стрик меньше цели - достижение не выдаётся"""
        mock_achievement_streak.goal=14
        with patch('backend.core.achievement_service.TrackingDAO') as mock_tracking:
            mock_tracking.get_user_longest_streak=AsyncMock(return_value=10)
            result=await AchievementService._check_longest_streak(mock_user, mock_achievement_streak)
            assert result is False

    @pytest.mark.asyncio
    async def test_check_longest_streak_goal_zero_returns_false(self, mock_user, mock_achievement_streak):
        """Проверяет: goal=0 всегда возвращает False"""
        mock_achievement_streak.goal=0
        with patch('backend.core.achievement_service.TrackingDAO') as mock_tracking:
            mock_tracking.get_user_longest_streak=AsyncMock(return_value=100)
            result=await AchievementService._check_longest_streak(mock_user, mock_achievement_streak)
            assert result is False


    """Тесты для check_and_award_achievements"""
    @pytest.mark.asyncio
    async def test_check_and_award_achievements_user_not_found(self):
        """Проверяет: пользователь не найден - возвращает пустой список"""
        with patch('backend.core.achievement_service.UserDAO') as mock_user_dao:
            mock_user_dao.find_one_or_none=AsyncMock(return_value=None)
            result=await AchievementService.check_and_award_achievements(user_id=999)
            assert result==[]
    
    @pytest.mark.asyncio
    async def test_check_and_award_achievements_all_already_earned(self, mock_user, mock_achievement, mock_achievement_streak):
        """Проверяет: все достижения уже получены - новых не выдаётся"""
        all_achievements=[mock_achievement, mock_achievement_streak]
        with patch('backend.core.achievement_service.UserDAO') as mock_user_dao, \
             patch('backend.core.achievement_service.AchievementDAO') as mock_achievement_dao, \
             patch('backend.core.achievement_service.UserAchievementsDAO') as mock_user_achievements_dao, \
             patch.object(AchievementService, '_check_achievement_condition') as mock_check:
            mock_user_dao.find_one_or_none=AsyncMock(return_value=mock_user)
            mock_achievement_dao.find_all=AsyncMock(return_value=all_achievements)
            mock_user_achievements_dao.find_user_all=AsyncMock(return_value=[
                MagicMock(achievement_id=1),
                MagicMock(achievement_id=2)
            ])
            result=await AchievementService.check_and_award_achievements(user_id=1)
            mock_check.assert_not_called()
            mock_user_achievements_dao.add.assert_not_called()
            assert result==[]
        
    @pytest.mark.asyncio
    async def test_check_and_award_achievements_new_achievement_awarded(self, mock_user, mock_achievement):
        """Проверяет: выдаётся новое достижение, если выполнено условие"""
        all_achievements=[mock_achievement]
        with patch('backend.core.achievement_service.UserDAO') as mock_user_dao, \
             patch('backend.core.achievement_service.AchievementDAO') as mock_achievement_dao, \
             patch('backend.core.achievement_service.UserAchievementsDAO') as mock_user_achievements_dao, \
             patch.object(AchievementService, '_check_achievement_condition') as mock_check:
            mock_user_dao.find_one_or_none=AsyncMock(return_value=mock_user)
            mock_achievement_dao.find_all=AsyncMock(return_value=all_achievements)
            mock_user_achievements_dao.find_user_all=AsyncMock(return_value=[])
            mock_check.return_value=True 
            mock_user_achievements_dao.add=AsyncMock(return_value=MagicMock())
            result=await AchievementService.check_and_award_achievements(user_id=1)
            mock_check.assert_called_once_with(mock_user, mock_achievement)
            mock_user_achievements_dao.add.assert_called_once_with(
                user_id=1,
                achievement_id=mock_achievement.id
            )
            assert len(result)==1
            assert result[0]==mock_achievement
    
    @pytest.mark.asyncio
    async def test_check_and_award_achievements_condition_not_met(self, mock_user, mock_achievement):
        """Проверяет: достижение не выдаётся, если условие не выполнено"""
        all_achievements=[mock_achievement]
        with patch('backend.core.achievement_service.UserDAO') as mock_user_dao, \
             patch('backend.core.achievement_service.AchievementDAO') as mock_achievement_dao, \
             patch('backend.core.achievement_service.UserAchievementsDAO') as mock_user_achievements_dao, \
             patch.object(AchievementService, '_check_achievement_condition') as mock_check:
            mock_user_dao.find_one_or_none=AsyncMock(return_value=mock_user)
            mock_achievement_dao.find_all=AsyncMock(return_value=all_achievements)
            mock_user_achievements_dao.find_user_all=AsyncMock(return_value=[])
            mock_check.return_value=False 
            result=await AchievementService.check_and_award_achievements(user_id=1)
            mock_check.assert_called_once_with(mock_user, mock_achievement)
            mock_user_achievements_dao.add.assert_not_called()
            assert result==[]
    

    """Тесты для _check_achievement_condition"""
    @pytest.mark.asyncio
    async def test_check_achievement_condition_profile_type(self, mock_user, mock_achievement):
        """Проверяет: для типа PROFILE_FILLED вызывается _check_profile_filled"""
        mock_achievement.type=AchievementTypes.PROFILE_FILLED
        with patch.object(AchievementService, '_check_profile_filled') as mock_check:
            mock_check.return_value=True
            result=await AchievementService._check_achievement_condition(mock_user, mock_achievement)
            mock_check.assert_called_once_with(mock_user, mock_achievement)
            assert result is True
    
    @pytest.mark.asyncio
    async def test_check_achievement_condition_streak_type(self, mock_user, mock_achievement):
        """Проверяет: для типа LONGEST_STREAK вызывается _check_longest_streak"""
        mock_achievement.type=AchievementTypes.LONGEST_STREAK
        with patch.object(AchievementService, '_check_longest_streak') as mock_check:
            mock_check.return_value=True
            result=await AchievementService._check_achievement_condition(mock_user, mock_achievement)
            mock_check.assert_called_once_with(mock_user, mock_achievement)
            assert result is True
    
    @pytest.mark.asyncio
    async def test_check_achievement_condition_unknown_type(self, mock_user, mock_achievement):
        """Проверяет: неизвестный тип возвращает False"""
        mock_achievement.type="unknown_type"
        result=await AchievementService._check_achievement_condition(mock_user, mock_achievement)
        assert result is False


