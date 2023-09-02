from telegram import Update
from telegram.ext import ContextTypes
from shelf import Record


def get_track_file_ids(recordID: int) -> list[int]:
    record = Record.by_id(recordID)
    for track in record.tracks:
        yield track.file_id


async def send_album(album_id: int, update: Update):
    tracks = get_track_file_ids(album_id)
    try:
        message = update.callback_query.message
    except AttributeError:
        message = update.message
    for file_id in tracks:
        await message.reply_audio(
                audio=file_id,
        )
    await message.reply_text(
            text="Enjoy 😊",
    )
