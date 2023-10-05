from fastapi import APIRouter, Depends, HTTPException, Header
from .dtos import Todo, DefualtResponseModel
from to_do_app.dependencies.dependencies import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from sqlalchemy import select, delete, update, insert
from to_do_app.db.models import Users, Todos, Shared

router = APIRouter(
    responses={404: {"detail": "Not found"}},
)

SECRET_KEY = "3cb260cf64fd0180f386da0e39d6c226137fe9abf98b738a70e4299e4c2afc93"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_current_user(token: str = Header(default=None)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return (username)

@router.post("/add_task")
async def add_task(item: Todo, user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    day = item.day
    task = item.task
    stmt = select(Users.user_id).where(Users.username == user)
    user_id = await session.scalar(stmt)
    new_task = Todos(day = day, task = task, user_id = user_id)
    session.add(new_task)
    await session.commit()

    return DefualtResponseModel(data = "task added successfully")

@router.post("/today_tasks")
async def today_tasks(day: str, user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = select(Users.user_id).where(Users.username == user)
    user_id = await session.scalar(stmt)
    if day == "All":
        stmt = select(Todos.task).where(Users.user_id == user_id)
        result = await session.scalars(stmt)
        tasks = result.all()
        return DefualtResponseModel(data=tasks)
    stmt = select(Todos.task).where(Todos.day == day).where(Users.user_id == user_id)
    result = await session.scalars(stmt)
    tasks = result.all()
    return DefualtResponseModel(data=tasks)

@router.post("/remove_task")
async def remove_task(item: Todo, user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    task = item.task
    day = item.day
    stmt = select(Users.user_id).where(Users.username == user)
    user_id = await session.scalar(stmt)
    stmt = delete(Todos).where(Todos.day == day).where(Todos.task == task).where(Todos.user_id == user_id)
    await session.execute(stmt)
    await session.commit()

    return DefualtResponseModel(data="task removed successfully")

@router.post("/share")
async def share(item: str, user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = select(Users.user_id).where(Users.username == user)
    user_id = await session.scalar(stmt)
    stmt = select(Users.user_id).where(Users.username == item)
    friend_id = await session.scalar(stmt)
    new_friend = Shared(user_id = user_id, friends_id = friend_id)
    session.add(new_friend)
    await session.commit()

    return DefualtResponseModel(data = "to do list shared")

@router.post("/see_friends_lists")
async def see_friends_lists(item: str, user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = select(Users.user_id).where(Users.username == user)
    user_id = await session.scalar(stmt)
    stmt = select(Users.user_id).where(Users.username == item)
    friend_id = await session.scalar(stmt)
    stmt = select(Shared.friends_id).where(Users.user_id == user_id)
    list_of_shared = await session.scalars(stmt)

    if user_id not in list_of_shared:
        return DefualtResponseModel(data="this user didn't share their tasks with you")
    else:
        stmt = select(Todos.task).where(Todos.user_id == friend_id)
        result = await session.scalars(stmt)
        tasks = result.all()
        return DefualtResponseModel(data = tasks)

    

    