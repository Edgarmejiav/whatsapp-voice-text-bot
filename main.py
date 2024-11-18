from fastapi import FastAPI, Request
from twilio.rest import Client
from dotenv import load_dotenv
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth
import logging

import requests
import os
import re
from datetime import datetime

from text import recognize_speech

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

audio_dir = os.path.join(os.getcwd(), "audios")
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

def generate_unique_filename(from_number: str, audio_dir: str, file_extension: str) -> str:

    cleaned_from_number = re.sub(r'\D', '', from_number)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{cleaned_from_number}_{timestamp}.{file_extension}"
    full_path = os.path.join(audio_dir, filename)

    return full_path

def save_audio_from_url(media_url: str, filename: str) -> bool:
    try:
        response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token))
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            logger.info(f"Audio saved as {filename}")
            return True
        else:
            logger.error(f"Failed to download audio. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error downloading or saving audio: {e}")
        return False

async def process_received_message(request: Request) -> dict:
    form_data = await request.form()
    from_number = form_data.get('From')
    body = form_data.get('Body')

    logger.info(f"Received message from {from_number}: {body}")
    media_url = form_data.get('MediaUrl0')  # Para el primer archivo multimedia

    if media_url:
        media_content_type = form_data.get('MediaContentType0')
        file_extension = media_content_type.split('/')[1]  # MP3, OGG, etc.
        filename = generate_unique_filename(from_number, audio_dir, file_extension)

        if save_audio_from_url(media_url, filename):
            result = recognize_speech(filename)
            return result
        else:
            return {"message": "Failed to save audio"}
    else:
        logger.warning("No media found in the message.")
        return {"message": "No audio found in the message"}

@app.post("/")
async def receive_sms(request: Request):
    body =  await process_received_message(request)
    client.messages.create(
        body=body,
        from_=twilio_number,
        to='whatsapp:+51949638354'
    )
    return {"message": "SMS processed"}
@app.post("/send_sms")
def send_sms():
    message = client.messages.create(
        body='Hello there!',
        from_=twilio_number,
        to='whatsapp:+51949638354'
    )
    return {"status": "success", "message": message.body}