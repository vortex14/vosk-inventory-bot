import telebot
import wave
import json
from number_extractor import read_message, NumberExtractor
import os

TOKEN = os.environ["TOKEN"] 
CHAT_ID = os.environ["CHAT_ID"] 

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

bot = telebot.TeleBot(TOKEN)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{msg_id}/{file_id}")
def read_root(file_id: str, msg_id: str, request: Request):

    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)
    
    with open(f'audios/{msg_id}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    os.system(f'ffmpeg -i ./audios/{msg_id}.ogg -ar 16000 -ac 1 -ab 192K -f wav ./decoded/{msg_id}.wav')
    wf = wave.open(f"decoded/{msg_id}.wav", "rb")

    rec = read_message(wf)

    data = rec.FinalResult()
    
    os.remove(f"decoded/{msg_id}.wav")
    os.remove(f"audios/{msg_id}.ogg")

    answer = json.loads(data)

    extractor = NumberExtractor()

    return {"data": extractor.replace_groups(answer["text"])}

