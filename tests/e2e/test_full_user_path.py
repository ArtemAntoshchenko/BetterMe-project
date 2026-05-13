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

    async def test_complete_registration_and_login_flow(self, page: Page, live_server: str):
        """E2E: Полная регистрация и вход пользователя (через UI)"""
        
        # Переход на главную и регистрация через UI
        await page.goto(f'{live_server}/')
        await expect(page.locator('h1')).to_contain_text('Трекер полезных привычек')
        await page.click('#link_to_main')
        await expect(page).to_have_url(f'{live_server}/auth/registration')

        timestamp = int(time.time())
        short_timestamp = str(timestamp)[-5:]
        test_data = {
            "nickname": f"e2e_{short_timestamp}",  
            "login": f"user_{short_timestamp}",     
            "password": "TestPass1231",
            "email": f"e2e_{short_timestamp}@test.com",
            "phone_number": f"+7{short_timestamp}12345",
            "first_name": "E2E",
            "last_name": "User",
            "city": "Test City",
            "date_of_birth": "1990-01-01"
        }

        # Заполнение формы регистрации
        await page.fill('#nickname', test_data['nickname'])
        await page.fill('#login', test_data['login'])
        await page.fill('#password', test_data['password'])
        await page.fill('#email', test_data['email'])
        await page.fill('#phone_number', test_data['phone_number'])
        await page.fill('#first_name', test_data['first_name'])
        await page.fill("#last_name", test_data["last_name"])
        await page.fill("#city", test_data["city"])
        await page.fill("#date_of_birth", test_data["date_of_birth"])

        await page.click('#reg-button')
        await page.wait_for_timeout(3000)
        await expect(page).to_have_url(f'{live_server}/auth/login')

        # Вход через UI
        await page.fill('#login', test_data['login'])
        await page.fill('#password', test_data['password'])
        
        async with page.expect_navigation():
            await page.click('#login-button')

        # Проверяем успешный вход (увеличиваем таймаут из-за мокнутого API)
        await expect(page).to_have_url(f'{live_server}/dashboard/main', timeout=10000)
        await expect(page.locator('h1', has_text='Добрый день!')).to_be_visible()
        await expect(page.locator('#logout-button')).to_be_visible(timeout=10000)

        # Выход
        async with page.expect_navigation():
            await page.click('#logout-button')

        await expect(page).to_have_url(f'{live_server}/auth/login')