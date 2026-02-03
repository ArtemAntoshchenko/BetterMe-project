from fastapi import APIRouter, Request, Depends
import os
from ..core.weather_api import WeatherClient
from ..routers.auth import getUserInfo
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ..db.database import *
from zoneinfo import ZoneInfo
from datetime import timedelta
from ..DAO.dao_habits import HabitDAO
from ..schemas.model_schemas.habit_schema import HabitSchema

router=APIRouter(prefix='/dashboard', tags=['Дашборд'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def dashBoard(request: Request, profile=Depends(getUserInfo)):
    weather_client=WeatherClient(base_url='https://api.openweathermap.org')
    weather_info=await weather_client.get_info(profile_data=profile)
    user_timezone=str(request.cookies.get('timezone', 'UTC'))
    timezone=ZoneInfo(user_timezone)
    tomorrow=datetime.now(timezone)+timedelta(days=1)
    tomorrow_date_str=tomorrow.date().strftime('%Y-%m-%d')
    forecasts=[]
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
        "js_url": "/static/js",
        "css_url": "/static/css",
        "weather_info": city_weather,
        "profile": profile
    }
    return templates.TemplateResponse('dashboard.html', context)

@router.get('/main/getActiveHabits')
async def getActiveHabits():
    result=await HabitDAO.find_all_active()
    return [{
        'id': habit.id,
        'name': habit.name,
        'description': habit.description,
        'complit_today': habit.complit_today,
        'progress': habit.progress,
        'goal': habit.goal
    } for habit in result]

@router.post('/main/complitActiveHabit/{habit_id}')
async def complitActiveHabit(habit_id: int):
    await HabitDAO.complit_habit(habit_id)
    return {'message': 'Привычка на сегодня выполнена'}

@router.post('/main/dailyUpdate/{habit_id}')
async def dailyHabitStatusUpdate(habit_id: int):
    await HabitDAO.daily_habit_status_update(habit_id)
    return {'message': 'Прошёл день и статус привычки был обновлён'}