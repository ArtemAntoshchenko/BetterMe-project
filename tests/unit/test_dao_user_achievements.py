import pytest
from datetime import date
from tests.conftest import AchievementTestDAO


class TestUserAchievementsDAO:

    async def test_find_user_all_return_all_user_achievements(self, db_session):
        """UserAchievementsDAO.find_user_all(): должен вернуть """