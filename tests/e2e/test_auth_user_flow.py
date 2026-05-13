import pytest
from playwright.async_api import Page, expect
from datetime import datetime
import time
import httpx
import random
import string

pytestmark=pytest.mark.e2e

class TestBetterMeE2E:
    """Набор E2E тестов для BetterMe"""

    async def test_authenticated_user_flow(self, page: Page, live_server, authenticated_user_e2e):
        """E2E: Тест для уже авторизованного пользователя (через UI с готовой сессией)"""
        
        # Устанавливаем токен в браузер
        await page.context.add_cookies([{
            "name": "users_access_token",
            "value": authenticated_user_e2e['token'],
            "url": live_server
        }])
        
        # Переходим на дашборд
        await page.goto(f'{live_server}/dashboard/main')
        
        # Проверяем, что пользователь авторизован
        await expect(page.locator('#logout-button')).to_be_visible()
        await expect(page.locator('.user-info')).to_contain_text(authenticated_user_e2e['nickname'])
        
        # Выход
        async with page.expect_navigation():
            await page.click('#logout-button')
        
        await expect(page).to_have_url(f'{live_server}/auth/login')