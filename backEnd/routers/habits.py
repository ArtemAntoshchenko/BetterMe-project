from fastapi import APIRouter, Request, Depends
import os
from os.path import dirname, abspath
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..db.database import *
from ..db.models import Habit
from ..schemas.service_schemas.update_habit_schema import HabitUpdateSchema, HabitResponseSchema
from ..schemas.model_schemas.habit_schema import HabitSchema
from ..DAO.dao_habits import HabitDAO

router=APIRouter(prefix='/habits', tags=['Привычки'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')
js_path=os.path.join(base_dir,'..','..','frontEnd','static','js')
templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def habits(request: Request):
    context={
        "request": request,
        "js_url": js_path
    }
    return templates.TemplateResponse('habits.html', context)

@router.get('/main/getHabits')
async def getHabits()-> list[HabitSchema]:
    return HabitDAO.find_all()

@router.get('/main/getActiveHabits')
async def getActiveHabits()-> list[HabitSchema]:
    return HabitDAO.find_all_active()

@router.put("/main/updateHabit", response_model=HabitResponseSchema)
async def updateHabit(habit: HabitUpdateSchema)-> HabitResponseSchema:
    update_data = habit.model_dump(exclude_none=True)
    habit_id = update_data.pop('id')
    result=await HabitDAO.update(filter_by={'habit_id': habit_id}, **update_data)                              
    return result

@router.delete("/main/delete/{habit_id}")
async def deleteHabit(habit_id: int)-> dict:
    result=await HabitDAO.delete(id=habit_id)
    if result:
        return {"message": f"Привычка с ID {habit_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении привычки!"}