from fastapi import APIRouter, Request
import os
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.database import *

router=APIRouter(prefix='/dashboard', tags=['Дашборд'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')
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
async def dashboard(request: Request):
    context={
        "request": request,
        "js_url": js_path
    }
    return templates.TemplateResponse('dashboard.html', context)

@router.get('/main/habist_list')
async def dashboard():
    context={
        "request": request,
        "js_url": js_path
    }
    return templates.TemplateResponse('dashboard.html', context)