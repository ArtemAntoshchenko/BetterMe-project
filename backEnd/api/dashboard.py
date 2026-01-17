from fastapi import APIRouter
import os
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

router=APIRouter(prefix='/dashboard', tags=['Дашборд'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_page','dashboard.html')

if os.path.exists(html_path):
    router.mount('/', StaticFiles(directory=os.path.dirname(html_path), html=True))
else:
    print(f'файл не найден:{html_path}')

@router.get('/main')
async def dashboard():
    return FileResponse(html_path)
