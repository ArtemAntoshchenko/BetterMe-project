from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from ..core.auth import get_password_hash
from ..DAO.dao_registration import UserDAO
from ..schemas.service_schemas.reg_schema import UserRegisterSchema, UserAuthSchema
from ..core.auth import authenticate_user, create_access_token, get_current_user
from ..db.models import User
from fastapi.templating import Jinja2Templates
from os.path import dirname, abspath
import os


router=APIRouter(prefix='/auth', tags=['Авторизация'])
base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','auth')
templates=Jinja2Templates(directory=html_path)

@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(name='login.html', context={'request': request, "js_url": "/static/js", "css_url": "/static/css"})

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
    return templates.TemplateResponse(name='registration.html', context={'request': request, "js_url": "/static/js", "css_url": "/static/css"})

@router.post('/registration')
async def registerUser(user_data: UserRegisterSchema)-> dict:
    user_login=await UserDAO.find_one_or_none(login=user_data.login)
    if user_login:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_email=await UserDAO.find_one_or_none(email=user_data.email)
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Эта почта уже занята'
        )
    user_nickname=await UserDAO.find_one_or_none(nickname=user_data.nickname)
    if user_nickname:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Этот никнейм уже занят'
        )
    user_phone_number=await UserDAO.find_one_or_none(phone_number=user_data.phone_number)
    if user_phone_number:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Этот номер уже занят'
        )
    user_dict=user_data.model_dump()
    user_dict['password']=get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.get("/user")
async def getUserInfo(user_data: User=Depends(get_current_user)):
    return user_data

@router.delete("/user/delete/{user_id}")
async def deleteUser(user_id: int)-> dict:
    result=await UserDAO.delete(id=user_id)
    if result:
        return {"message": f"Пользователь с ID {user_id} удалён!"}
    else:
        return {"message": "Ошибка при удалении пользователя!"}
