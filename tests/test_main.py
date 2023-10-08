from jose import jwt
from starlette.testclient import TestClient
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

SECRET_KEY = "3cb260cf64fd0180f386da0e39d6c226137fe9abf98b738a70e4299e4c2afc93"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@pytest.mark.anyio
async def test_add_user(test_app: AsyncClient):
    response = await test_app.post(
        "/users/add_user",
        json={"username":"user123", "password":"user123!", "email":"user123@y.ru"},
    )
    assert response.status_code == 200
    assert response.json() == {"data":'User added succesfully'}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@pytest.mark.anyio
async def test_authenticate_user(test_app: AsyncClient):
    response = await test_app.post(
        "/users/authenticate_user",
        json={"username":"user", "password":"user!", "email":"user123@y.ru"},
    )
    assert response.status_code == 200
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
    data={"sub": "user"}, expires_delta=access_token_expires
    )
    assert response.json() == {
        "data":{
            "access_token": access_token,
            "token_type": "bearer"
        }
    }

@pytest.mark.anyio
async def test_add_task(test_app: AsyncClient):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
    data={"sub": "user"}, expires_delta=access_token_expires
    )
    response = await test_app.post(
        "/todo/add_task",
        headers={"token": access_token},
        json={"day":"Monday", "task":"drink_beer"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "data":
            "task added successfully"
        }
    
@pytest.mark.anyio
async def test_add_task(test_app: AsyncClient):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
    data={"sub": "user"}, expires_delta=access_token_expires
    )
    response = await test_app.post(
        "/todo/today_tasks",
        params={"day":"Monday"},
        headers={"token": access_token}
    )
    assert response.status_code == 200
    assert response.json() == {
        "data":
            []}
        




