from starlette.testclient import TestClient
import pytest
from to_do_app.app import app
from to_do_app.db.models import db_meta
from sqlalchemy.ext.asyncio import AsyncEngine,AsyncSession,create_async_engine,async_sessionmaker,AsyncTransaction
from typing import AsyncGenerator
import os
from to_do_app.dependencies.dependencies import get_async_session
from httpx import AsyncClient
from passlib.hash import pbkdf2_sha256
from to_do_app.db.models import Users, Todos


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"

@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:

    engine = create_async_engine(str(os.environ.get("DB_DSN")))
    async with engine.begin() as conn:
        await conn.run_sync(db_meta.create_all)

    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(db_meta.drop_all)
        await engine.dispose()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()
    hashed_password = pbkdf2_sha256.hash("user!")
    new_user = Users(username = "user", password = hashed_password, email = "user@y.ru",share = 1)
    session.add(new_user)
    await session.commit()

    try:
        yield session
    finally:
        await session.close()
        await try_rollback(trans)
        await connection.close()


async def try_rollback(rollbackable: AsyncSession | AsyncTransaction) -> None:
    try:
        await rollbackable.rollback()
    except Exception:
        return
    

@pytest.fixture(scope="function")
async def test_app(dbsession: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: dbsession

    async with AsyncClient(app = app, base_url="http://test") as client:
        yield client





