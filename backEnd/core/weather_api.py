from aiohttp import ClientSession
from fastapi import Depends
from ..core.config import settings


class WeatherClient():
    def __init__(self, base_url:str):
        self.base_url=base_url
        
    async def get_info(self, profile_data):
        async with ClientSession(base_url=self.base_url) as session:
            async with session.get(f'/data/2.5/forecast?q={profile_data.city}&units=metric&appid={settings.API_KEY}') as respons:
                result=await respons.json()
                return result
