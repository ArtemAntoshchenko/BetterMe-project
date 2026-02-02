from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base, int_pk, str_uniq, int_null_true, bool_False
from datetime import date

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    nickname: Mapped[str_uniq]
    login: Mapped[str_uniq]
    password: Mapped[str]
    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    city: Mapped[str]
    date_of_birth: Mapped[date]
    premium: Mapped[bool]=mapped_column(default=False)

class Habit(Base):
    __tablename__ = 'habits'

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str]=mapped_column(Text)
    complit: Mapped[bool_False]
    complit_today: Mapped[bool_False]
    goal: Mapped[int_null_true]
    progress: Mapped[int]=mapped_column(default=0)
    step: Mapped[int_null_true]


