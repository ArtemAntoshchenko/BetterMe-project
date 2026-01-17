from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers.auth import router as router_auth
from routers.dashboard import router as router_dashboard
import os
from os.path import dirname, abspath

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','frontEnd','public','landing','index.html')

app=FastAPI()

if os.path.exists(html_path):
    app.mount('/', StaticFiles(directory=os.path.dirname(html_path), html=True))
else:
    print(f'файл не найден:{html_path}')
@app.get('/')
async def landing_page():
    return FileResponse(html_path)

app.include_router(router_auth)
app.include_router(router_dashboard)