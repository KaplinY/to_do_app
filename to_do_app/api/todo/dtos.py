from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class Todo(BaseModel):
    day: str
    task: str

class DefualtResponseModel(BaseModel, Generic[T]):
    data: Optional[T] = None