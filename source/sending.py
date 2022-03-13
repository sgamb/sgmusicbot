import logging
import os

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram import Bot

from shelf import engine, Track


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))


def send_track(file_id, chat_id):
    """ Sends one track by its file_id """
    try:
        bot.send_audio(chat_id, audio=file_id)
    except Exception as err:
        logging.error(err)


def send_record(record_id, chat_id):
    """ Sends all tracks from album by given record_id """
    with Session(engine) as session:
        stmt = select(Track.file_id).where(Track.record_id == record_id)
        result = session.execute(stmt)
        for file_id in result.scalars().all():
            send_track(file_id, chat_id)
