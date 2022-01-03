import os
import random

from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, Updater

from filters import record_id_filter
from sending import send_info, send_record
import shelf

load_dotenv()

TOKEN = os.getenv('TOKEN')

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def handle_record_id(update, context):
    record_id = update.message.text
    send_record(record_id, update.message.from_user.id)


def handle_start(update, context):
    send_info('hi', update.message.from_user.id)


def handle_random(update, context):
    number_of_records = shelf.count_records()
    random_record_id = random.randint(1, number_of_records)
    send_record(random_record_id, update.message.from_user.id)


start_handler = CommandHandler('start', handle_start)
random_handler = CommandHandler('random', handle_random)
record_id_handler = MessageHandler(record_id_filter, handle_record_id)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(random_handler)
dispatcher.add_handler(record_id_handler)

updater.start_polling()
