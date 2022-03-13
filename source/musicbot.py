import os
import random

from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, Updater

import filters
import sending
import shelf

load_dotenv()

updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher


def handle_record_id(update):
    record_id = update.message.text
    sending.send_record(record_id, update.message.from_user.id)


def handle_start(update, context):
    context.bot.send_message(text='hi', chat_id=update.message.from_user.id)


def handle_random(update):
    number_of_records = shelf.count_records()
    random_record_id = random.randint(1, number_of_records)
    sending.send_record(random_record_id, update.message.from_user.id)


record_id_handler = MessageHandler(filters.record_id_filter, handle_record_id)
start_handler = CommandHandler('start', handle_start)
random_handler = CommandHandler('random', handle_random)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(random_handler)
dispatcher.add_handler(record_id_handler)

updater.start_polling()
