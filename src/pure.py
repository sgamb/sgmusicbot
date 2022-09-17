import os
from dotenv import load_dotenv
import asyncio
import telegram


async def main():
    load_dotenv()
    bot = telegram.Bot(os.getenv('TOKEN'))
    async with bot:
        # await bot.send_message(text='Hello, John', chat_id=144407396)

        print((await bot.getUpdates(
            offset=77824976,
            limit=1,
            timeout=3,
            allowed_updates=["message"],
        ))[0])


if __name__ == '__main__':
    asyncio.run(main())
