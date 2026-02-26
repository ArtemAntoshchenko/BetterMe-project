from fastapi import APIRouter, Request, Depends, HTTPException, status
import os
from .auth import getUserInfo
from os.path import dirname, abspath
from ..core.auth import get_password_hash
from fastapi.templating import Jinja2Templates
from ..db.database import *
from ..DAO.dao_registration import UserDAO
from ..core.redis import cache
from ..schemas.model_schemas.user_schema import UserSchema
from ..schemas.service_schemas.profile_update_schema import ProfileUpdateSchema, ProfileUpdateResponse

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
    info=await UserDAO.find_one_or_none(id=profileId)
    return info

@router.put('/main/info/update')
async def profileInfoUpdate(profile: ProfileUpdateSchema)-> ProfileUpdateResponse:
    update_info=profile.model_dump(exclude_none=True)
    profile_id=update_info.pop('id')
    if 'phone_number' in update_info:
        existing_phone_number = await UserDAO.find_one_or_none(
            phone_number=update_info['phone_number']
        )
        if existing_phone_number and existing_phone_number.id != profile_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Этот номер телефона уже занят другим пользователем'
            )
    if 'email' in update_info:
        existing_email = await UserDAO.find_one_or_none(
            email=update_info['email']
        )
        if existing_email and existing_email.id != profile_id:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Эта почта уже занята другим пользователем'
        )
    if 'nickname' in update_info:
        existing_nickname = await UserDAO.find_one_or_none(
            nickname=update_info['nickname']
        )
        if existing_nickname and existing_nickname.id != profile_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Этот никнейм уже занят другим пользователем'
            )
    update_info['password']=get_password_hash(profile.password)
    result=await UserDAO.update(filter_by={'id':profile_id}, **update_info)
    return result