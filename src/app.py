import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def lucky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You are lucky today :)")

if __name__ == '__main__':
    load_dotenv()
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    lucky_handler = CommandHandler('lucky', lucky)
    application.add_handler(lucky_handler)
    
    application.run_polling()
