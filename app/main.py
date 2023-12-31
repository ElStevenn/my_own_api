#!/usr/bin/env python3

from fastapi import FastAPI, File, UploadFile,WebSocket, Request 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse 
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketState 
from api import email_sender, openai_translator
from pathlib import Path
from pydantic import BaseModel
import uvicorn 
import os


app = FastAPI( debug=True
)
    
class Translater(BaseModel):
	 text_to_translate:str

_email_sender = email_sender.EmailSender()
# This is not working! But i have to fix it!

app.mount("/static", 
StaticFiles(directory="static"), name="static")

# CORS origins setup (though you're allowing all 
# origins in the middleware)
origins = [ "http://localhost", 
    "http://localhost:8000", "http://127.0.0.1", 
    "http://127.0.0.1:8000",
]

app.add_middleware( CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"])

@app.get("/")
async def home():
	with  open(os.path.join(os.path.dirname(__file__), "front_end", "file.html"), 'r') as file:
		html_content = file.read()
	return HTMLResponse(content=html_content)

@app.get("/projects") 
async def projects():
	with open(os.path.join(os.path.dirname(__file__), "front_end", "projects.html"), 'r') as file:
		html_content = file.read()
	return HTMLResponse(content=html_content)

@app.get("/translator") 
async def translator():
    with open(Path("front_end/translator.html"),'r') as file:
        html_content = file.read() 
    return HTMLResponse(content=html_content)

# @app.get("/api") async def api_projection():
#    return HTMLResponse("<h1> - under    construction - </h1>")

# @app.post("/send_email") async def 
# send_an_email(schemas.EmailBasicStructure):
#     """""" return {"return": "Under 
#     construction"}


@app.get("/get_publicssh") 
async def get_public_ssh_key():
	with open(os.path.join(Path("/files/mamadoKey.txt.pub"))) as f:
		public_key = f.read()
	return PlainTextResponse(public_key)

@app.get("/cv") 
async def show_cv():
	file_path = os.path.join(os.path.dirname(__file__), "Pau_Mateu_Resume.pdf")
	return FileResponse(file_path)

@app.get("/cv-es") 
async def show_cv():
	file_path = os.path.join(os.path.dirname(__file__),"Pau_Mateu_Resume_esp.pdf")
	 # Change this to the other resume 
	return FileResponse(file_path)

@app.get("/iq") 
async def show_iq():
	path = os.path.join(os.path.dirname(__file__),"files", "8328_certificat.pdf")
	return FileResponse(path)


@app.get("/download_pgp_key") 
async def download_pgp_key():
	file_path = os.path.join(os.path.dirname(__file__), "files", "mamadoKey.txt") 
	return FileResponse(file_path)


@app.get("/file/{filename}") 
async def get_file(filename: str):
	try:
		file_path = os.path.join(os.path.dirname(__file__),"files", filename)
		if not os.path.exists(file_path):
			return {"error": f"the filename {filename} doesn't exist"}
		return FileResponse(file_path)
	except Exception as e: 
		return {"error": f"An error occurred: {str(e)}"}


@app.get("/send", response_class=HTMLResponse) 
async def send_email():
	return HTMLResponse("<h1>implement this option</h1>")

# @app.post("/send_email", description="Method 
# to send an email, this is an intern method") 
# async def send_body_email(body_request: 
# schemas.EmailBasicStructure)-> dict:
#     try: _email_sender.send_email(body_request.to, 
#         body_request.subject, 
#         body_request.text or '')
#     except Exception as e: return 
#         {"status":"error","response":f"An 
#         error ocurred {e}"}
#     return 
#     {"status":"sucsess","response":"Email has 
#     been sended succesfully"}

@app.get("/justdeleteme")
async def deletememe():
	file_path = os.path.join(os.path.dirname(__file__),"files", "joebiden.png")
	return FileResponse(file_path)


@app.get("/send_email") 
async def emailsender():
	with open(os.path.join(os.path.dirname(__file__), "front_end", "send_email.html"), 'r') as file:
		html_content = file.read() 
	return HTMLResponse(html_content)


@app.websocket("/ws_endpoint_translate")
async def translate_text(websocket: WebSocket):
	await websocket.accept() 
	client_host = websocket.client.host 
	try:
		while True:
			data = await websocket.receive_json() 
			if 'text_to_translate' in data and 'origin_language' in data and 'language_to_translate' in data:
				translated_text = await openai_translator.translate_text_with_gpt4( 
                  client_host, 
                   data['text_to_translate'], 
                   data['origin_language'], 
                   data['language_to_translate'],
               ) 
				await websocket.send_json({"translated_text": translated_text})
			else: 
				await websocket.send_json({"error": "Invalid data format"})
			
	except Exception as e: 
		await websocket.send_json({"error": str(e)})

	finally: 
		if websocket.application_state !=  WebSocketState.DISCONNECTED:
			await websocket.close()



# ----------------------------- Mini functions 
# -----------------------------------------------------------------


if __name__ == "__main__":
    # uvicorn main:app --host 0.0.0.0 --port 80 
    # PostgreSQL file conf -> 
    # /etc/postgresql/14/main/postgresql.conf
    uvicorn.run( "main:app", host = "0.0.0.0", 
        port = 443, # remember to use 443 port when ssl has been using
        ssl_keyfile = 
        "/home/ubuntu/certificates/paumateu.key", 
        # Place here ssl key file path 
        ssl_certfile = 
        "/home/ubuntu/certificates/www_paumateu_com.crt", 
        # Place here ssl certificate path 
        reload=True
    )
