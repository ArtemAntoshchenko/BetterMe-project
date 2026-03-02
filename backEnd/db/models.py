from sqlalchemy import Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base, int_pk, str_uniq, int_null_true, bool_False
from datetime import date, datetime
from typing import List

class Achievement(Base):
    __tablename__ = 'achievements'

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str]=mapped_column(Text)
    goal: Mapped[int]=mapped_column(default=0)
    users: Mapped[List['UserAchievements']]=relationship(back_populates='achievement', cascade='all, delete-orphan')

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
    super_user: Mapped[bool]=mapped_column(default=False, nullable=True)
    achievements: Mapped[List['UserAchievements']]=relationship(back_populates='user', cascade='all, delete-orphan')

    @property
    def has_achievements(self)-> bool:
        return len(self.achievements)>0

class UserAchievements(Base):
    __tablename__ = 'user_achievements'

    id: Mapped[int_pk]
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    achievement_id: Mapped[int]=mapped_column(ForeignKey('achievements.id', ondelete='CASCADE'))
    obtained: Mapped[bool_False]
    user: Mapped[User]=relationship(back_populates='completions')
    achievement: Mapped[Achievement]=relationship(back_populates='users')

    __table_args__ = (
        UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement'),
    )

class Habit(Base):
    __tablename__ = 'habits'

    id: Mapped[int_pk]
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str_uniq]
    description: Mapped[str]=mapped_column(Text)
    complit: Mapped[bool_False]
    complit_today: Mapped[bool_False]
    goal: Mapped[int_null_true]
    progress: Mapped[int]=mapped_column(default=0)
    step: Mapped[int_null_true]
    completions: Mapped[List['HabitCompletion']]=relationship(back_populates='habit', cascade='all, delete-orphan')

    @property
    def has_completions(self)-> bool:
        return len(self.completions)>0

class HabitCompletion(Base):
    __tablename__ = 'habit_completions'

    id: Mapped[int_pk]
    habit_id: Mapped[int]=mapped_column(ForeignKey('habits.id', ondelete='CASCADE'))
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    completed_date: Mapped[date]=mapped_column(default=date.today)
    completed_at: Mapped[datetime]=mapped_column(default=datetime.now)
    current_streak: Mapped[int]=mapped_column(default=0)
    longest_streak: Mapped[int]=mapped_column(default=0)
    habit: Mapped[Habit]=relationship(back_populates='completions')
