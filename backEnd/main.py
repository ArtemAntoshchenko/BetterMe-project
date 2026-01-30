from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .routers.auth import router as router_auth
from .routers.dashboard import router as router_dashboard
from .routers.dashboard import router as router_dashboard
from .routers.habits import router as router_habits
from .routers.tracking import router as router_tracking
import os
from os.path import dirname, abspath

app=FastAPI()
app.include_router(router_auth)
app.include_router(router_dashboard)
app.include_router(router_habits)
app.include_router(router_tracking)


base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','frontEnd','public','landing','index.html')

public_dir = os.path.join(base_dir, '..', 'frontEnd', 'public', 'lending')
if os.path.exists(public_dir):
    app.mount('/public', StaticFiles(directory=public_dir), name='public')

static_dir = os.path.join(base_dir, '..', 'frontEnd', 'static', 'js')
if os.path.exists(static_dir):
    app.mount('/static/js', StaticFiles(directory=static_dir), name='static')

static_dir = os.path.join(base_dir, '..', 'frontEnd', 'static', 'css')
if os.path.exists(static_dir):
    app.mount('/static/css', StaticFiles(directory=static_dir), name='static')

@app.get('/')
async def landing_page():
    return FileResponse(html_path)


