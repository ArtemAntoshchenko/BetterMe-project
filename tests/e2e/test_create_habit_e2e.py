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
        await expect(page.locator('h2', has_text='Все привычки:')).to_be_visible()
        
        # Переходим на страницу создания новой привычки
        await page.click('#create-button')
        await expect(page.locator('h1', has_text='Создание привычки:')).to_be_visible()

        # Создаём новую привычку
        await page.fill('#name', 'E2E Test Habit2')
        await page.fill('#description', 'Created by E2E test3')
        await page.fill('#goal', '100')
        await page.fill('#step', '10')
        await page.click('#create-button')
        
        # Проверяем, что привычка создалась
        await page.goto(f'{live_server}/habits/main')
        await page.wait_for_timeout(2000)
        await expect(page.locator('h2', has_text='Все привычки:')).to_be_visible()
        tbody = page.locator('#tbodyHabits')
        await expect(tbody).to_contain_text('E2E Test Habit2', timeout=10000)
