import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.ext import CommandHandler as ch

from main import get_track_file_ids

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update.to_json())
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm a bot, please talk to me!",
    )


async def lucky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command handler that send random album.. or not?"""
    albumID = random.randint(1, 100)
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(albumID),
    )

    if albumID <= 35:
        trackFileIDs = get_track_file_ids(albumID)
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="OK, sending audio",
        )
        for fileID in trackFileIDs:
            await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=fileID,
            )
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are lucky today :)",
        )
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, no luck :(",
        )

if __name__ == '__main__':
    load_dotenv()
    app = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    start_handler = ch('start', start)
    app.add_handler(start_handler)
    lucky_handler = ch('lucky', lucky)
    app.add_handler(lucky_handler)

    app.run_polling()
