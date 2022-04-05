import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from shelf import Record, Track, engine
from sqlalchemy.orm import Session
from telegram import Bot

load_dotenv()

CHAT_ID = os.environ.get('CHAT_ID')
bot = Bot(token=os.getenv('TOKEN'))

parser = argparse.ArgumentParser(description='upload files to telegram server')
parser.add_argument('path', type=Path, help='directory to upload', nargs='*')


def record_disk(album_dir):
    """ Create new DISK and start track recording """
    year = os.path.basename(os.path.dirname(album_dir))
    album = os.path.basename(album_dir)
    with Session(engine) as session:
        disk = Record(year=year, record_name=album)
        session.add(disk)
        record_tracks_of(disk, album_dir, session)
        session.commit()


def record_tracks_of(record, album_dir, session):
    """ Create new Track instance for each sent track """
    bot.send_message(chat_id=CHAT_ID, text=record.record_name)
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
    """ Collect MP3s from given Path """
    track_list = []
    files = os.listdir(album_dir)
    for file_name in sorted(files):
        if file_name.endswith('.mp3'):
            track_list.append(file_name)
    return track_list


def send_file(mp3):
    """ Upload the file to telegram and return its id """
    with open(mp3, 'rb') as audio:
        try:
            msg = bot.send_audio(CHAT_ID, audio)
            return msg.audio.file_id
        except Exception as err:
            logging.error(err)


if __name__ == '__main__':
    args = parser.parse_args()
    for path in args.path:
        record_disk(path)
