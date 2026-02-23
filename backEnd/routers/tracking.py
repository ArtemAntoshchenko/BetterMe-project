from fastapi import APIRouter, Request, Depends, HTTPException, Query
import os
from os.path import dirname, abspath
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ..db.database import *
from ..DAO.dao_habits import HabitDAO
from ..DAO.dao_tracking import TrackingDAO
from ..schemas.model_schemas.completion_habit_schema import HabitCompletionSchema, AllHabitsCompletionSchema
from ..routers.auth import getUserInfo
from typing import Optional

router=APIRouter(prefix='/tracking', tags=['Отслеживание привычек'])

base_dir=os.path.dirname(os.path.abspath(__file__))
html_path=os.path.join(base_dir,'..','..','frontEnd','public','main_pages')

templates=Jinja2Templates(directory=html_path)

@router.get('/main')
async def tracking(request: Request, profile=Depends(getUserInfo)):
    context={
        "request": request,
        'js_url': '/static/js',
        'css_url': '/static/css',
        "profile": profile
    }
    return templates.TemplateResponse('tracking.html', context)

@router.get('/main/{habit_id}/heatmap', response_model=HabitCompletionSchema)
async def get_habit_heatmap(habit_id: int, days: Optional[int]=Query(365, ge=7, le=730), profile=Depends(getUserInfo)):
    habit=await HabitDAO.find_one_or_none(id=habit_id, user_id=profile.id)
    if not habit:
        raise HTTPException(status_code=404, detail='Привычка не найдена')
    heatmap_data=await TrackingDAO.get_heatmap_data(habit_id, days)
    stats=await TrackingDAO.get_heatmap_stats(habit_id, days)
    return HabitCompletionSchema(
        habit_id=habit.id,
        user_id=profile.id,
        habit_name=habit.name,
        habit_description=habit.description,
        goal=habit.goal,
        progress=habit.progress,
        step=habit.step,
        heatmap_data=heatmap_data,
        current_streak=stats['current_streak'],
        longest_streak=stats['longest_streak'],
        total_completions=stats['total_completions'],
        completion_rate=stats['completion_rate']
    )

@router.get('/main/heatmaps', response_model=AllHabitsCompletionSchema)
async def get_all_habits_heatmaps(days: Optional[int]=Query(90, ge=7, le=365), profile=Depends(getUserInfo)):
    habits_data=await TrackingDAO.get_all_habits_heatmap_data(days)
    return AllHabitsCompletionSchema(habits=habits_data)

