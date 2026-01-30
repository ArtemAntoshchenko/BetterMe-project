from aiohttp import ClientSession
from ..db.models import User
from ..core.config import settings


class WeatherClient():
    def __init__(self, base_url:str):
        self.base_url=base_url

    async def get_info(self):
        async with ClientSession(base_url=self.base_url) as session:
            async with session.get(f'/data/2.5/forecast?q=London&units=metric&appid={settings.API_KEY}') as respons:
                result=await respons.json()
                return result
