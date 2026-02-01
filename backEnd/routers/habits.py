from fastapi import APIRouter, Request, Depends, HTTPException, status
import os
from os.path import dirname, abspath
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..db.database import *
from ..db.models import Habit
from ..schemas.service_schemas.update_habit_schema import HabitUpdateSchema, HabitUpdateResponse 
from ..schemas.service_schemas.create_habit_schema import HabitCreateSchema
from ..schemas.model_schemas.habit_schema import HabitSchema
from ..DAO.dao_habits import HabitDAO
from ..routers.auth import getUserInfo

router=APIRouter(prefix='/habits', tags=['Привычки'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')
templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def habits(request: Request, profile=Depends(getUserInfo)):
    context={
        "request": request,
        "js_url": "/static/js",
        "css_url": "/static/css",
        "profile": profile
    }
    return templates.TemplateResponse('habits.html', context)

@router.get('/main/getHabits')
async def getHabits()-> list[HabitSchema]:
    habits=await HabitDAO.find_all()
    return habits

@router.get('/main/getActiveHabits')
async def getActiveHabits()-> list[HabitSchema]:
    habits_active=await HabitDAO.find_all_active()
    return habits_active

@router.get('/main/createNewHabit')
async def createNewHabit(request: Request):
    return templates.TemplateResponse(name='new_habit.html', context={'request': request, "js_url": "/static/js", "css_url": "/static/css"})

@router.post('/main/createNewHabit')
async def createNewHabit(habit_data: HabitCreateSchema)-> dict:
    habit=await HabitDAO.find_one_or_none(name=habit_data.name)
    if habit:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Привычка с таким названием уже существует'
        )
    habit_dict=habit_data.model_dump()
    await HabitDAO.add(**habit_dict)
    return {'message': 'Вы успешно создали привычку!'}

@router.put("/main/updateHabit", response_model=HabitUpdateResponse)
async def updateHabit(habit: HabitUpdateSchema)-> HabitUpdateResponse:
    update_data = habit.model_dump(exclude_none=True)
    habit_id = update_data.pop('id')
    result=await HabitDAO.update(filter_by={'id': habit_id}, **update_data)                              
    return result

@router.delete("/main/delete/{habit_id}")
async def deleteHabit(habit_id: int)-> dict:
    result=await HabitDAO.delete(id=habit_id)
    if result:
        return {"message": f"Привычка с ID {habit_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении привычки!"}