from .dao_base import BaseDAO
from ..db.models import Achievement
from ..db.database import get_db
from sqlalchemy import select

class AchievementDAO(BaseDAO):
    model=Achievement
        
