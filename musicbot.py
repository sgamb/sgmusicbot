import os
import logging

from pathlib import Path
from telegram import Bot
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from shelf import Record, Track


""" ###########CONF########### """

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DB_URL = os.getenv('DB_URL')
HOME_DIR = os.getenv('HOME_DIR')

bot = Bot(token=TOKEN)
engine = create_engine(DB_URL, echo=True, future=True)


""" ###########FUNC########### """


def do_record(record, album_dir, session):
    """ Record each track of album """
    tracks = get_tracks(album_dir)
    for track_name in tracks:
        mp3 = album_dir / track_name
        file_id = send_file(mp3)
        track = Track(
            record_id=record.id,
            track_name=track_name,
            file_id=file_id,
        )
        session.add(track)
        session.flush()


def get_tracks(album_dir):
    """ Collect mp3 from album directory """
    track_list=[]
    files = os.listdir(album_dir)
    for file_name in sorted(files):
        if file_name.endswith('.mp3'):
            track_list.append(file_name)
    return track_list


def send_file(mp3):
    """ Send file to telegram and return file_id """
    with open(mp3, 'rb') as audio:
        try:
            msg = bot.send_audio(CHAT_ID, audio)
            return msg.audio.file_id
        except Exception as err:
            logging.error(err)


def populate_database():
    """ Read the file system and record every album """
    home_dir = Path(HOME_DIR)
    years = os.listdir(home_dir)

    session = Session(engine)

    for year in sorted(years):
        year_dir = home_dir / year
        albums = os.listdir(year_dir)
        for album in sorted(albums):
            album_dir = year_dir / album

            disk = Record(year=year, record_name=album)
            session.add(disk)
            session.flush()

            do_record(disk, album_dir, session)
            session.commit()

    session.close()


def send_track(file_id, chat_id=CHAT_ID):
    """ Sends one track by its file_id """
    try:
        msg = bot.send_audio(chat_id, audio=file_id)
    except Exception as err:
        logging.error(err)


def send_record(record_id, chat_id=CHAT_ID):
    """ Sends all tracks from album by given record_id """
    with Session(engine) as session:
        stmt = select(Track.file_id).where(Track.record_id == record_id)
        result = session.execute(stmt)
        for file_id in result.scalars().all():
            send_track(file_id, chat_id)
