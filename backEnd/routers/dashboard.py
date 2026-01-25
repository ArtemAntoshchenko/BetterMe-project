from fastapi import APIRouter, Request, Depends
import os
from core.weather_api import WeatherClient
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.database import *
from zoneinfo import ZoneInfo
from datetime import timedelta


router=APIRouter(prefix='/dashboard', tags=['Дашборд'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')
if os.path.exists(html_path):
    router.mount('/main', StaticFiles(directory=os.path.dirname(html_path)))
else:
    print(f'файл не найден:{html_path}')

js_path=os.path.join(base_dir,'..','..','frontEnd','static','js')
if os.path.exists(js_path):
    router.mount('/main', StaticFiles(directory=os.path.dirname(js_path)))
else:
    print(f'файл не найден:{js_path}')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def dashboard(request: Request):
    weather_client=WeatherClient(base_url='https://api.openweathermap.org')
    weather_info=await weather_client.get_info()
    user_timezone=str(request.cookies.get('timezone', 'UTC'))
    tz=ZoneInfo(user_timezone)
    tomorrow=datetime.now(tz)+timedelta(days=1)
    tomorrow_date_str=tomorrow.date().strftime('%Y-%m-%d')
    forecasts=[]
    if 'list' in weather_info:
        for forecast in weather_info['list']:
            if 'dt_txt' in forecast:
                forecast_date=forecast['dt_txt'].split()[0]  
                if forecast_date==tomorrow_date_str:
                    weather={
                        'datetime': forecast['dt_txt'],
                        'temperature': forecast['main']['temp'],
                        'description': forecast['weather'][0]['description'],
                        'icon': forecast['weather'][0]['icon']
                    }
                    forecasts.append(weather)
    city_weather=forecasts[4]
    context={
        "request": request,
        "js_url": js_path,
        "weather_info": city_weather
    }
    return templates.TemplateResponse('dashboard.html', context)

# @router.get('/main/habits_daily_list')
# async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
#     return await StudentDAO.find_all(**request_body.to_dict())