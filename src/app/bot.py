from src.app.loader import bot, dp


class TelegramParser:
    async def start(self):
        await dp.start_polling(bot)
