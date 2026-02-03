from .dao_base import BaseDAO
from ..db.models import User

 
class UserDAO(BaseDAO):
    model=User