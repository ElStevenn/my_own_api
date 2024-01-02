import asyncio
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, crud

async def get_city_country(ip: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}") as res:
            result = await res.json()
            return result.get('country', None), result.get('city', None)

async def fetch_log_update(db: AsyncSession, id: str, ip: str):
    # Retrieve the record
    client_country, client_city = await get_city_country(ip)
    stmt = select(models.Translator_logs).where(models.Translator_logs.id == id)
    result = await db.execute(stmt)
    record = result.scalars().first()

    if record:
        # Modify the record
        record.client_country = client_country[:20] if client_country else None
        record.client_city = client_city[:20] if client_country else None

        # Commit the changes
        await db.commit()
        await db.refresh(record)
        return record
    else:
        return None

async def update_old_row(db: AsyncSession):
    all_rows = await crud.get_all_logs(db)
    return all_rows

async def old():
    # Create a separate session for fetching logs
    db_gen = crud.get_db()
    db = await db_gen.__anext__()
    try:
        logs = await update_old_row(db)
    finally:
        await db_gen.aclose()

    all_ids_to_update = [(log.id, log.client_ip) for log in logs if not log.client_city or not log.client_country]

    # Process each update in a separate session
    for id_, ip_ in all_ids_to_update:
        db_gen = crud.get_db()
        db = await db_gen.__anext__()
        try:
            log = await fetch_log_update(db=db, id=id_, ip=ip_)
            if log:
                print(f"Updated log ID: {log.id}")
            else:
                print("Log not found or update failed.")
        finally:
            await db_gen.aclose()



# Add Zip and using phoene field


 
# async def main():
#     db_gen = crud.get_db()
#     db = await db_gen.__anext__()
#     try:
#         logs = await update_old_row(db)
#     finally:
#         await db_gen.aclose()







if __name__ == "__main__":
    asyncio.run(main())
