from src.app.loader import bot, dp


class TelegramParser:
    """This class represents a parser for handling Telegram messages"""
    async def start(self):
        """
        Asynchronously start polling for Telegram messages.

        This method activates the bot to continuously check for and respond to incoming messages.
        """
        await dp.start_polling(bot)
