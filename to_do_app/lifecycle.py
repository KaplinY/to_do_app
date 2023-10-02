from fastapi import APIRouter, FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractIncomingMessage
from aio_pika.pool import Pool
from taskiq_aio_pika import AioPikaBroker


def init_app(app: FastAPI): 
    @app.on_event("startup")
    async def _startup_event():
        engine = create_async_engine(
        os.environ.get("DB_DSN"), echo = True,
        )
        app.state.db_engine = engine

        app.state.async_sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False
        )
    
        


        

            
        

        

