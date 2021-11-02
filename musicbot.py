import os
import logging

from pathlib import Path
from telegram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from shelf import Record, Track


""" ###########CONF########### """

bot = Bot(token=os.getenv('TOKEN'))
chat_id = os.getenv('CHAT_ID')

db_url = os.getenv('DB_URL')
engine = create_engine(db_url, echo=True, future=True)


""" ###########FUNC########### """


def do_record(record, album_dir, session):
    """ Record each track of album """
    tracks = get_tracks(album_dir)
    for track_name in tracks:
        mp3 = album_dir / track_name
        file_id = send_track(mp3)
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


def send_track(mp3):
    """ Send file to telegram and return file_id """
    with open(mp3, 'rb') as audio:
        try:
            msg = bot.send_audio(chat_id, audio)
            return msg.audio.file_id
        except Exception as err:
            logging.error(err)


""" ###########MAIN########### """


def main():
    """ Read the file system and record every album """
    HOME_DIR = Path('/home/serge/Music/Collection')
    years = os.listdir(HOME_DIR)

    session = Session(engine)

    for year in sorted(years):
        year_dir = HOME_DIR / year
        albums = os.listdir(year_dir)
        for album in sorted(albums):
            album_dir = year_dir / album

            disk = Record(year=year, record_name=album)
            session.add(disk)
            session.flush()
            do_record(disk, album_dir, session)
            session.commit()

    session.close()


if __name__ == '__main__':
    main()


""" ###########TEST########### """


def test():
    year = 'y_2020'
    album = 'Паша Жданов - Частности и детали, Ч.1'
    album_dir = Path('/home/serge/Music/Паша Жданов - Частности и детали, Ч.1')

    session = Session(engine)

    disk = Record(year=year, record_name=album)
    session.add(disk)
    do_record(disk, album_dir, session)

    session.flush()
    session.commit()
    session.close()
