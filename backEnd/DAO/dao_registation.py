from .dao_base import BaseDAO
from ..db.models import User

 
class UserDAO(BaseDAO[User]):
    def __init__(self):
        super().__init__(User)