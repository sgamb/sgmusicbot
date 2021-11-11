import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telegram import Bot

from shelf import Record, Track

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DB_URL = os.getenv('DB_URL')
HOME_DIR = os.getenv('HOME_DIR')

bot = Bot(token=TOKEN)
engine = create_engine(DB_URL, echo=True, future=True)


def read_home_dir():
    """ Read the file system and record every album from each year

├── 1965
│   └── The Beatles - Rubber Soul
├── 1966
│   ├── Bob Dylan - Blonde On Blonde
│   ├── Fresh Cream - Cream
│   └── ...
└── ...

    """
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

            record_tracks_of(disk, album_dir, session)
            session.commit()

    session.close()


def record_tracks_of(record, album_dir, session):
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
    """ Collect MP3s from album directory """
    track_list = []
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


if __name__ == '__main__':
    print('Are you shure you want to start music collecting? [y/n]: ', end='')
    answer = input()
    if answer in 'yY':
        read_home_dir()
    else:
        print('Canceled')
