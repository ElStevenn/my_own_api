import asyncio
import openai
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
from .sql_app import crud, schemas
import re

api_key = "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"


async def remove_main_brackets(text):
    # Remove contents within round and square brackets including the brackets
    return re.sub(r'\[.*?\]|\(.*?\)', '', text)

async def store_data(client_ip, origin_language, language_to_translate, origin_text, translated_text):
    async for db in crud.get_db():
        # Create a new log item using the schema
        new_log = schemas.CreateItemLod(
            ip=client_ip, 
            origin_language=origin_language, 
            language_to_translate=language_to_translate,
            origin_text=origin_text, 
            translated_text=translated_text
        )
        
        # Create the log entry in the database
        await crud.create_log(db, new_log)
        break  
    

async def translate_text_with_gpt4(client_ip, text_to_translate, origin_language="English", language_to_translate="Spanish",):
    openai.api_key = "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"
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




if __name__ == "__main__":
    text_to_translate = r"""
    El mejor experto financiero ha empezado a estudiar, investigar y seguir los consejos de verdaderos expertos

    Ha llegado a la conclusión de que #Bitcoin (+150% de subida este año) no le interesa

    Le interesa más comprar Bitcoin Cash o Chainlink jajajajaja
    Translate post
        """
    
    async def main():
        return await translate_text_with_gpt4(text_to_translate, origin_language="Spanish", language_to_translate="English")

    translated_text = asyncio.run(main())
    print(translated_text)