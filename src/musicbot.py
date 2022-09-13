import logging
import os
import random

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram import Update
from telegram.user import User
from telegram.ext import CommandHandler, MessageHandler, Updater, CallbackContext

from filters import record_id_filter
from shelf import Record, engine

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def start(update: Update, _context: CallbackContext) -> None:
    """Check the user and reply 'hi' to the '/start' command"""
    user: User = update.effective_user
    logging.info(f'Start from {user.to_json()=}')
    user.send_message('Hi!')


def lucky(update: Update, _context: CallbackContext) -> None:
    """Send random record"""
    number_of_records = Record.get_number_of_records()
    record_id = random.randint(1, number_of_records)
    send_record(update, record_id)


def handle_record_id(update: Update, _context: CallbackContext) -> None:
    """Get record id as message text and send the record"""
    record_id = int(update.message.text)
    send_record(update, record_id)


def handle_list(update: Update, _context: CallbackContext) -> None:
    """Select records and send their names"""
    records = Record.get_record_list()
    for record in records:
        update.message.reply_text(record.record_name)


def send_record(update: Update, record_id: int) -> None:
    """Selecting a recording and sending tracks from it"""
    stmt = select(Record).where(Record.id == record_id)
    with Session(engine) as session:
        record = session.scalar(stmt)
        for track in record.tracks:
            update.message.reply_audio(track.file_id)


def experiment(update: Update, _context: CallbackContext):
    update.message.reply_text("Are you admin?")
    if update.effective_user.id == os.getenv('CHAT_ID'):
        print("I'm gonna destroy you")
    else:
        logging.info(update.effective_user.id, os.getenv('CHAT_ID'))


def main() -> None:
    """Start the bot"""
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('lucky', lucky))
    dispatcher.add_handler(MessageHandler(record_id_filter, handle_record_id))
    dispatcher.add_handler(CommandHandler('list', handle_list))
    dispatcher.add_handler(CommandHandler('admin', experiment))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
