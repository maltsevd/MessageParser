import asyncio
from src.app import TelegramParser

# Entry point for the script
if __name__ == '__main__':
    # Initialize the TelegramParser instance
    bot = TelegramParser()

    # Start the Telegram bot using asynchronous execution
    asyncio.run(bot.start())
