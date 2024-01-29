import asyncio
import openai
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
from .sql_app import crud, schemas
import re, aiohttp
from .enviroment import env_variable

api_key = env_variable["TRANSLATOR_APIKEY"]


async def remove_main_brackets(text):
    # Remove contents within round and square brackets including the brackets
    return re.sub(r'\[.*?\]|\(.*?\)', '', text)

async def get_client_data(ip: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,mobile,query") as res:
            result = await res.json()
            return result.get('country', None), result.get('city', None), result.get('zip', None), result.get('mobile', None)



async def store_data(client_ip, origin_language, language_to_translate, origin_text, translated_text):
    async for db in crud.get_db():
        # Get country, zipcode, mobile (if the user is u)
        country, city, zipcode, mobile = await get_client_data(client_ip)
        country = country[:50] if country else None
        city = city[:50] if city else None
        zip_code = zipcode[:50] if city else None
        mobie = mobile if mobile else None

        # Create a new log item using the schema
        new_log = schemas.CreateItemLod(
            ip=client_ip, 
            origin_language=origin_language, 
            language_to_translate=language_to_translate,
            origin_text=origin_text, 
            translated_text=translated_text,
            client_country=country,
            client_city=city,
            client_zip_code=zip_code,
            using_phone=mobie
        )
        
        # Create the log entry in the database
        await crud.create_log(db, new_log)
        break

    

async def translate_text_with_gpt4(client_ip, text_to_translate, origin_language="English", language_to_translate="Spanish",):
    openai.api_key =  env_variable["TRANSLATOR_APIKEY"]
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        response = await loop.run_in_executor(
            pool,
            lambda: openai.ChatCompletion.create(
                model="gpt-4",  # Replace with the correct model name
                messages=[{"role": "user", "content": f'Translate the following {origin_language} text to {language_to_translate}: "{text_to_translate}"'}]
            )
        )

        # Extract the translated text
        translated_text = await remove_main_brackets(response['choices'][0]['message']['content'])

        # Check if translated_text is a string
        if not isinstance(translated_text, str):
            translated_text = str(translated_text)  # Convert to string if necessary

        # Store the data into the database
        asyncio.create_task(store_data(client_ip=client_ip, origin_language=origin_language, language_to_translate=language_to_translate, origin_text=text_to_translate, translated_text=translated_text))

        return translated_text


async def main():
    ip = "92.189.163.252"
    country, city, zipcode, mobile  = await get_client_data(ip)
    print(country);print(city);print(zipcode);print(mobile);

if __name__ == "__main__":
    asyncio.run(main())