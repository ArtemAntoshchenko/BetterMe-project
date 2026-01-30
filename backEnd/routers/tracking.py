from fastapi import APIRouter, Request, Depends
import os
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ..db.database import *

router=APIRouter(prefix='/tracking', tags=['Отслеживание привычек'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')
js_path=os.path.join(base_dir,'..','..','frontEnd','static','js')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def tracking(request: Request):
    context={
        "request": request,
        "js_url": js_path
    }
    return templates.TemplateResponse('tracking.html', context)


