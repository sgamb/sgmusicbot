import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from telegram import Bot

from shelf import Track

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DB_URL = os.getenv('DB_URL')

engine = create_engine(DB_URL, echo=True, future=True)

bot = Bot(token=TOKEN)


def send_info(text, chat_id=CHAT_ID):
    bot.send_message(text=text, chat_id=chat_id)


def send_track(file_id, chat_id=CHAT_ID):
    """ Sends one track by its file_id """
    try:
        bot.send_audio(chat_id, audio=file_id)
    except Exception as err:
        logging.error(err)


def send_record(record_id, chat_id=CHAT_ID):
    """ Sends all tracks from album by given record_id """
    with Session(engine) as session:
        stmt = select(Track.file_id).where(Track.record_id == record_id)
        result = session.execute(stmt)
        for file_id in result.scalars().all():
            send_track(file_id, chat_id)
