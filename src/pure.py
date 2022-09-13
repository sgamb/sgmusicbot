import os
from dotenv import load_dotenv
import asyncio
import telegram


async def main():
    load_dotenv()
    bot = telegram.Bot(os.getenv('TOKEN'))
    async with bot:
        await bot.send_message(text='Hello, John', chat_id=144407396)


if __name__ == '__main__':
    asyncio.run(main())
