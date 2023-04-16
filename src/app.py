import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.ext import CommandHandler as ch

from main import send_album
from conversation import years_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update.to_json())
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hi. Please, use the other command",
    )


async def lucky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command handler that send random album.. or not?"""
    album_id = random.randint(1, 100)
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(album_id),
    )
    if 35 < album_id <= 65:
        await send_album(album_id, update)
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, no luck :(",
        )


async def album(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (len(context.args) != 1):
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Usage: /album 13",
        )
        return
    album_id = int(context.args[0])
    await send_album(album_id, update)

if __name__ == '__main__':
    print('starting')
    load_dotenv()
    app = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    app.add_handler(ch('start', start))
    app.add_handler(ch('lucky', lucky))
    app.add_handler(ch('album', album))
    app.add_handler(years_handler)
    app.run_polling(allowed_updates=[])
