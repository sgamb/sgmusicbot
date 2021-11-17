import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, Updater

from filters import record_id_filter
from sending import send_info, send_record

load_dotenv()

TOKEN = os.getenv('TOKEN')

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def send_record_by_id(update, context):
    record_id = update.message.text
    send_record(record_id)


def hi(update, context):
    send_info('hi')


record_id_handler = MessageHandler(record_id_filter, send_record_by_id)
start_handler = CommandHandler('start', hi)

dispatcher.add_handler(record_id_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
