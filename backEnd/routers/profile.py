from fastapi import APIRouter, Request, Depends
import os
from .auth import getUserInfo
from os.path import dirname, abspath
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

@router.get('/main')
async def profile(request: Request, profile=Depends(getUserInfo)):
    context={
        'request': request,
        'js_url': '/static/js',
        'css_url': '/static/css',
        'profile': profile
    }
    return templates.TemplateResponse('profile.html', context)

@router.get('/main/info')
async def profileInfo(profileId)-> UserSchema:
    info=await UserDAO.find_one_or_none(profileId)
    return info

@router.put('/main/info/update')
async def profileInfoUpdate(profile: ProfileUpdateSchema)-> ProfileUpdateResponse:
    update_info=profile.model_dump(exclude_none=True)
    profile_id=update_info.pop('id')
    result=await UserDAO.update(filter_by={'id':profile_id}, **update_info)
    return result