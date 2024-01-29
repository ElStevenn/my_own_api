from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from .models import *
import asyncio
from sqlalchemy import MetaData
from ..enviroment import env_variable

SQLALCHEMY_DATABASE_URL = str(env_variable["DATABASE_URL2"])
# Connection postgresql://<user>:<password>@<host>:<port>/<database_name>
# Port: 5432

# Removed connect_args as it's not needed for PostgreSQL
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False, 
    autoflush=False
)

Base = declarative_base()

async def get_all_table_names():
    async with async_engine.connect() as conn:
        meta = MetaData()
        await conn.run_sync(meta.reflect)
        return list(meta.tables.keys())

async def main():
    table_names = await get_all_table_names()
    print(table_names)

if __name__ == "__main__":
    print("****************************************************")
    asyncio.run(main())