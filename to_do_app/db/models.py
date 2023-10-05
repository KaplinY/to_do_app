from pydantic import BaseModel
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

db_meta = sa.MetaData() 

class Base(DeclarativeBase):
    metadata = db_meta 

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.String(100), unique=True)
    password: Mapped[str] = mapped_column(sa.Text)
    email: Mapped[str] = mapped_column(sa.Text, unique=True)
    share: Mapped[str] = mapped_column(sa.BigInteger())

class Todos(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    day: Mapped[str] = mapped_column(sa.Text)
    task: Mapped[str] = mapped_column(sa.Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped[Users] = relationship(Users, foreign_keys=[user_id], uselist=False)

class Shared(Base):
    __tablename__ = "shared"
    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    friends_id: Mapped[int] = mapped_column(sa.BigInteger())
    user: Mapped[Users] = relationship(Users, foreign_keys=[user_id], uselist=False)