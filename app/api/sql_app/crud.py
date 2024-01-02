from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from . import models, schemas, database
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    """Get database session"""
    async with database.AsyncSessionLocal() as db:
        yield db
    


async def get_all_logs(db: AsyncSession, skip: int = 0):

    result = await db.execute(select(models.Translator_logs)).offset(skip)
    return result.scalars().all()

async def get_all_by_ip(db: AsyncSession, ip:str):
    pass

async def get_by_id(db: AsyncSession, id: str):
    result = await db.execute(
        models.Translator_logs.select().where(models.Translator_logs.id == id)
    )
    return result.scalars().first()

async def create_log(db: AsyncSession, Log: schemas.CreateItemLod):
    # Get country and city by its ip
    # country, city = await get_city_country(Log.ip)

    db_log = models.Translator_logs(
        client_ip=Log.ip, 
        origin_language=Log.origin_language, 
        language_to_translate=Log.language_to_translate, 
        origin_text=Log.origin_text, 
        translated_text=Log.translated_text,
        client_country = Log.client_coutry,
        client_city = Log.client_city,
        zip_code = Log.client_zip_code,
        using_phone = Log.using_phone
    )
    
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log

async def delete_log_id(db: AsyncSession, id: str):
    try:
        log_to_delete = await get_by_id(db=db, id=id)
        await db.delete(log_to_delete)
        await db.commit()
        return f"Log {log_to_delete} deleted successfully"
    except Exception as e:
        return f"An error occurred: {e}"

async def delete_logs_ip(db: AsyncSession, ip: str):
    try:
        logs_to_delete = await get_all_by_ip(db=db, ip=ip)
        for log in logs_to_delete:
            await db.delete(log)
        await db.commit()
        return f"Logs from IP {ip} deleted successfully"
    except Exception as e:
        return f"An error occurred: {e}"



# Try the crud and database
if __name__ == "__main__":
    pass