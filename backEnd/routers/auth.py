from fastapi import APIRouter

router=APIRouter(prefix='/auth', tags=['Авторизация'])

@router.post('/login')
async def login():
    pass

@router.post('/registration')
async def registration():
    pass