from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from ..core.auth import get_password_hash
from ..DAO.dao_registation import UserDAO
from ..schemas.service_schemas.reg_schema import UserRegisterSchema, UserAuthSchema
from ..core.auth import authenticate_user, create_access_token, get_current_user
from ..db.models import User
from fastapi.templating import Jinja2Templates
from os.path import dirname, abspath
import os


router=APIRouter(prefix='/auth', tags=['Авторизация'])
base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','auth')
js_path=os.path.join(base_dir,'..','..','frontEnd','static','js')
css_path=os.path.join(base_dir,'..','..','frontEnd','static','css')
templates=Jinja2Templates(directory=html_path)

@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(name='login.html', context={'request': request, "js_url": js_path, "css_url": css_path})

@router.post('/login')
async def loginUser(response: Response, user_data: UserAuthSchema):
    check=await authenticate_user(login=user_data.login, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token=create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.post("/logout")
async def logoutUser(response: Response):
    response.delete_cookie(key="users_access_token", path="/")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get('/registration')
async def register(request: Request):
    return templates.TemplateResponse(name='registration.html', context={'request': request, "js_url": js_path, "css_url": css_path,})

@router.post('/registration')
async def registerUser(user_data: UserRegisterSchema) -> dict:
    user=await UserDAO.find_one_or_none(login=user_data.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict=user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.get("/me/")
async def getMe(user_data: User=Depends(get_current_user)):
    return user_data

