from typing import Generic, TypeVar, Type
from backEnd.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseDAO(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model=model