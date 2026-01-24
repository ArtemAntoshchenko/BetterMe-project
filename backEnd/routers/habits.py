from fastapi import APIRouter, Request, Depends
import os
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import *
from db.models import Habit

router=APIRouter(prefix='/habits', tags=['Привычки'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages', 'habits.html')
if os.path.exists(html_path):
    router.mount('/main', StaticFiles(directory=os.path.dirname(html_path), html=True))
else:
    print(f'файл не найден:{html_path}')

js_path=os.path.join(base_dir,'..','..','frontEnd','static','js')
if os.path.exists(js_path):
    router.mount('/main', StaticFiles(directory=os.path.dirname(js_path)))
else:
    print(f'файл не найден:{js_path}')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def habits(request: Request):
    context={
        "request": request,
        "js_url": js_path
    }
    return templates.TemplateResponse('habits.html', context)

@router.get('/main/getHabits')
async def getHabits(db: Session=Depends(get_db)):
    return db.query(Habit).all()

@router.get('/main/getActiveHabits')
async def getHabits(db: Session=Depends(get_db)):
    active_habits=db.query(Habit).filter(Habit.active==True).all()
    return active_habits
