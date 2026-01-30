from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .database import Base, int_pk, str_uniq, int_null_true, bool_False
from datetime import date

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    nickname: Mapped[str_uniq]
    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    city: Mapped[str]
    date_of_birth: Mapped[date]
    premium: Mapped[bool]
    auth: Mapped['Auth']=relationship('Auth', back_populates='user', uselist=False, cascade='all, delete-orphan')

class Auth(Base):
    __tablename__ = 'auth'

    id: Mapped[int_pk]
    login: Mapped[str_uniq]
    password: Mapped[str]
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id'))
    user: Mapped[User]=relationship('User', back_populates='auth', uselist=False)

class Habit(Base):
    __tablename__ = 'habits'

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str]=mapped_column(Text)
    active:Mapped[bool_False]
    complit: Mapped[bool_False]
    complit_today: Mapped[bool_False]
    goal: Mapped[int_null_true]
    progress: Mapped[int_null_true]


