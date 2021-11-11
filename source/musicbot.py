import logging
import os

from dotenv import load_dotenv
from telegram.ext import MessageHandler, Updater
from telegram.ext.filters import Filters

from sending import send_record

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def try_send_record_by_id(update, context):
    text = update.message.text
    try:
        record_id = int(text)
#       validate record_id
        send_record(record_id)
    except ValueError as err:
        context.bot.send_message(chat_id=CHAT_ID,
                                 text='That was not an integer')
        logging.error(err)


record_id_handler = MessageHandler(Filters.text, try_send_record_by_id)

dispatcher.add_handler(record_id_handler)

updater.start_polling()
