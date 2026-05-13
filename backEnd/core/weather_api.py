from aiohttp import ClientSession
from fastapi import Depends
from ..core.config import settings
from .redis import cache
import os
from datetime import datetime, timedelta

class WeatherClient():
    def __init__(self, base_url:str):
        self.base_url=base_url
        
    async def get_info(self, profile_data):
        if os.environ.get('TESTING')=='true' or os.environ.get('E2E_TESTING')=='true':
            return self._get_mock_weather()
        cache_key=f'weather:{profile_data.city}'
        cached=await cache.get(cache_key)
        if cached:
            return cached
        async with ClientSession(base_url=self.base_url) as session:
            async with session.get(f'/data/2.5/forecast?q={profile_data.city}&units=metric&appid={settings.API_KEY}') as respons:
                result=await respons.json()
                await cache.set(cache_key, result, expire=3600)
                return result
    
    def _get_mock_weather(self):
        return {
            "list": [
                {
                    "dt_txt": (datetime.now() + timedelta(days=1, hours=i)).strftime('%Y-%m-%d %H:%M:%S'),
                    "main": {"temp": 20 + i // 3},
                    "weather": [{"description": "test weather", "icon": "01d"}]
                }
                for i in range(0, 24, 3)
            ]
        }
