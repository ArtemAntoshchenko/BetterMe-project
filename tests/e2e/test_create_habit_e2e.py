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

    async def test_create_habit_e2e(self, page: Page, live_server, authenticated_user_e2e):
        """E2E: Полный цикл создания привычки через UI авторизованным пользователем"""
        
        # Устанавливаем токен
        await page.context.add_cookies([{
            "name": "users_access_token",
            "value": authenticated_user_e2e['token'],
            "url": live_server
        }])
        
        # Переходим на страницу привычек
        await page.goto(f'{live_server}/habits/main')
        await expect(page.locator('h1')).to_contain_text('Список привычек')
        
        # Создаём новую привычку (заполните селекторы под свои)
        await page.click('#create-habit-button')
        await page.fill('#habit-name', 'E2E Test Habit')
        await page.fill('#habit-description', 'Created by E2E test')
        await page.fill('#habit-goal', '100')
        await page.fill('#habit-step', '10')
        await page.click('#save-habit-button')
        
        # Проверяем, что привычка создалась
        await expect(page.locator('.habit-item')).to_contain_text('E2E Test Habit')