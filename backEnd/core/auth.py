from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from .config import get_auth_data
from ..DAO.dao_registation import UserDAO
from fastapi import Request, HTTPException, status, Depends

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(days=6)
    to_encode.update({"exp": expire})
    auth_data=get_auth_data()
    encode_jwt=jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

async def authenticate_user(login: str, password: str):
    user=await UserDAO.find_one_or_none(login=login)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

def get_token(request: Request)-> str:
    COOKIE_NAME="users_access_token"
    token=request.cookies.get(COOKIE_NAME)
    if not token and not token.strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не найден')
    return token

async def get_current_user(token: str=Depends(get_token)):
    try:
        auth_data=get_auth_data()
        payload=jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']], options={
                "verify_exp": True,
                "verify_signature": True,
                "require_sub": True,
            })
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный')
    user_id=payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    user=await UserDAO.find_one_or_none(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')
    return user