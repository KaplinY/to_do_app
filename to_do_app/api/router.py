from fastapi import APIRouter
from . import users
from to_do_app.api import todo


router = APIRouter()
router.include_router(users.router, prefix="/users")
router.include_router(todo.router, prefix="/todo")
