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