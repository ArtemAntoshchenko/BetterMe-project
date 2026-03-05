from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import os
from .auth import getUserInfo
from os.path import dirname, abspath
from ..core.auth import get_password_hash
from fastapi.templating import Jinja2Templates
from ..db.database import *
from ..DAO.dao_registration import UserDAO
from ..DAO.dao_user_achievements import UserAchievementsDAO
from ..core.redis import cache
from ..schemas.service_schemas.profile_update_schema import ProfileUpdateSchema, ProfileUpdateResponse
from ..core.achievement_service import AchievementService

router=APIRouter(prefix='/profile', tags=['Профиль'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')

templates=Jinja2Templates(directory=html_path)

@router.get('/main/{profileId}')
async def profile(request: Request, profile=Depends(getUserInfo)):
    context={
        'request': request,
        'js_url': '/static/js',
        'css_url': '/static/css',
        'profile': profile
    }
    return templates.TemplateResponse('profile.html', context)

@router.get('/main/{profileId}/info')
async def profileInfo(profileId: int):
    cache_key=f'profile:{datetime.now().date()}'
    cached=await cache.get(cache_key)
    if cached is not None:
        return cached
    profile=await UserDAO.find_one_or_none(id=profileId)
    await cache.set(cache_key, profile, expire=60)
    return profile

@router.put('/main/info/update')
async def profileInfoUpdate(profile: ProfileUpdateSchema)-> ProfileUpdateResponse:
    update_info=profile.model_dump(exclude_none=True)
    profile_id=update_info.pop('id')
    if 'phone_number' in update_info:
        existing_phone_number=await UserDAO.find_one_or_none(
            phone_number=update_info['phone_number']
        )
        if existing_phone_number:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Этот номер телефона уже занят другим пользователем'
            )
    if 'email' in update_info:
        existing_email=await UserDAO.find_one_or_none(
            email=update_info['email']
        )
        if existing_email:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Эта почта уже занята другим пользователем'
        )
    if 'nickname' in update_info:
        existing_nickname=await UserDAO.find_one_or_none(
            nickname=update_info['nickname']
        )
        if existing_nickname:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Этот никнейм уже занят другим пользователем'
            )
    update_info['password']=get_password_hash(profile.password)
    result=await UserDAO.update(filter_by={'id':profile_id}, **update_info)
    await cache.clear_pattern('profile:*')  
    return result

@router.get('/main/{profileId}/checkAchievements')
async def checkProfileAchievements(profileId: int):
    cache_key=f'checkAchievements:{datetime.now().date()}'
    cached=await cache.get(cache_key)
    if cached is not None:
        return cached
    new_achievements=await AchievementService.check_and_award_achievements(profileId)
    all_user_achievements=await UserAchievementsDAO.find_user_all(user_id=profileId)
    if not all_user_achievements:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Ни одного достижения ещё не было получено"}
        )
    await cache.set(cache_key, all_user_achievements, expire=60)
    return all_user_achievements
    