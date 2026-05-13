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

    async def test_api_registration_and_login(self, e2e_client, live_server):
        """E2E: Тестирование API регистрации и входа"""
        
        timestamp = int(time.time())
        short_timestamp = str(timestamp)[-5:]
        user_data = {
            "nickname": f"api_{short_timestamp}",
            "login": f"api_user_{short_timestamp}",
            "password": "TestPass123",
            "email": f"api_{short_timestamp}@test.com",
            "phone_number": f"+7{short_timestamp}12345",
            "first_name": "API",
            "last_name": "Test",
            "city": "Test City",
            "date_of_birth": "1990-01-01"
        }
        
        # Регистрация через API
        response = await e2e_client.post("/auth/registration", json=user_data)
        assert response.status_code == 200
        
        # Вход через API
        response = await e2e_client.post("/auth/login", json={
            "login": user_data["login"],
            "password": user_data["password"]
        })
        assert response.status_code == 200
        assert "access_token" in response.json()