from fastapi import APIRouter, Request, Depends
import os
from ..core.weather_api import WeatherClient
from .auth import getUserInfo
from os.path import dirname, abspath
from fastapi.templating import Jinja2Templates
from ..db.database import *
from zoneinfo import ZoneInfo
from datetime import timedelta
from ..DAO.dao_habits import HabitDAO
from ..DAO.dao_tracking import TrackingDAO
from ..core.redis import cache

router=APIRouter(prefix='/profile', tags=['Профиль'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def profile(request: Request, profile=Depends(getUserInfo)):
    context={
        'request': request,
        'js_url': '/static/js',
        'css_url': '/static/css',
        'profile': profile
    }
    return templates.TemplateResponse('profile.html', context)