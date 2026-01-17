# from fastapi import APIRouter
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# import os
# from os.path import dirname, abspath

# router=APIRouter(prefix='/landing', tags=['Лендинг'])

# base_dir=os.path.dirname(os.path.abspath(__file__))
# html_path=os.path.join(base_dir,'..','..','frontEnd','public','index.html')

# if os.path.exists(html_path):
#     router.mount('/', StaticFiles(directory=os.path.dirname(html_path), html=True))
# else:
#     print(f'файл не найден:{html_path}')

