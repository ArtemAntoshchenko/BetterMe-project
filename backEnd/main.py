from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .core.redis import cache
from .routers.auth import router as router_auth
from .routers.dashboard import router as router_dashboard
from .routers.dashboard import router as router_dashboard
from .routers.habits import router as router_habits
from .routers.tracking import router as router_tracking
from .routers.profile import router as router_profile
import os
from os.path import dirname, abspath

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    yield
    await cache.close()

app=FastAPI(lifespan=lifespan)
base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','frontEnd','public','landing')
public_dir = os.path.join(base_dir, '..', 'frontEnd', 'public')
static_dir = os.path.join(base_dir, '..', 'frontEnd', 'static')
templates=Jinja2Templates(directory=html_path)

if os.path.exists(public_dir):
    app.mount('/public', StaticFiles(directory=public_dir), name='public')

if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')

app.include_router(router_auth)
app.include_router(router_dashboard)
app.include_router(router_habits)
app.include_router(router_tracking)
app.include_router(router_profile)

@app.get('/')
async def landing_page(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request,"css_url": "/static/css"})


