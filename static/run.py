from src.app import TelegramParser
import asyncio


if __name__ == '__main__':
    bot = TelegramParser()
    asyncio.run(bot.start())
