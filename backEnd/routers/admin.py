from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import os
from .auth import getUserInfo
from os.path import dirname, abspath
from ..core.auth import get_password_hash
from fastapi.templating import Jinja2Templates
from ..db.database import *
from ..DAO.dao_registration import UserDAO
from ..DAO.dao_achievement import AchievementDAO
from ..core.redis import cache
from ..schemas.service_schemas.create_achievement_schema import CreateAchievementSchema
from ..schemas.service_schemas.achievement_type_schema import AchievementTypeResponse
from ..core.achievement_service import AchievementTypes

router=APIRouter(prefix='/admin', tags=['Админпанель'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def profile(request: Request):
    context={
        'request': request,
        'js_url': '/static/js',
        'css_url': '/static/css'
    }
    return templates.TemplateResponse('admin.html', context)

@router.get('/main/info')
async def profilesInfo():
    cache_key=f'profiles:all:{datetime.now().date()}'
    cached=await cache.get(cache_key)
    if cached is not None:
        return cached
    profiles=await UserDAO.find_all()
    await cache.set(cache_key, profiles, expire=60)
    return profiles

@router.delete('/main/delete/{user_id}')
async def profileDelete(user_id: int)-> dict:
    result=await UserDAO.delete(id=user_id)
    if result:
        return {"message": f"Профиль с ID {user_id} удалён!"}
    else:
        return {"message": "Ошибка при удалении профиля!"}

@router.put("/main/makeSuperuser/{user_id}")
async def makeSuperuser(user_id: int):
    new_superuser=await UserDAO.changeUserStatus(user_id)
    await cache.clear_pattern('profiles:*')                             
    return new_superuser
    
@router.get('/main/getAchievements')
async def getAchievements():
    cache_key=f'achievements:all:{datetime.now().date()}'
    cached=await cache.get(cache_key)
    if cached is not None:
        return cached
    achievements=await AchievementDAO.find_all()
    if not achievements:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Ни одного достижения ещё не было создано"}
        )
    await cache.set(cache_key, achievements, expire=60)
    return achievements

@router.post('/main/createAchievement')
async def createAchievement(achievement_data: CreateAchievementSchema)-> dict:
    achievement=await AchievementDAO.find_one_or_none(name=achievement_data.name)
    if achievement:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такое достижение уже существует'
        )
    achievement_dict=achievement_data.model_dump()
    await AchievementDAO.add(**achievement_dict)
    await cache.clear_pattern('achievements:all:*')
    return {'message': 'Вы успешно создали достижение!'}

@router.get('/main/getAchievementTypes', response_model=list[AchievementTypeResponse])
async def get_achievement_types():
    return AchievementTypes.get_all_types()

@router.delete('/main/deleteAchievement/{achievement_name}')
async def deleteAchievement(achievement_name: int)-> dict:
    result=await AchievementDAO.delete(name=achievement_name)
    if result:
        return {"message": f"Достижение {achievement_name} удалено!"}
    else:
        return {"message": "Ошибка при удалении достижения!"}

