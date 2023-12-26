import os
from aiogram import F, Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from loguru import logger
from src.parsers import ImageParser
from src.utils import saver
from app import BOT_TOKEN, YC_OAUTH, IMAGES_FOLDER, YC_FOLDER_ID

im_parser = ImageParser()

# Add logger to file with level INFO
logger.add("logs/logs_from_tg_bot.log", level="INFO")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
logger.info("Initialized Bot")


# Initialize dispatcher for bot. Dispatcher is a class that process
# all incoming updates and handle them to registered handlers
dp = Dispatcher()


@dp.message(F.text)
async def process_channel_messages(message: Message):
    try:
        # Extract message information
        message_text = message.text
        date = message.date.strftime("%Y-%m-%d %H:%M:%S")
        sender = message.from_user.username if message.from_user.username else "N/A"
        saver.save_message(message_text, date, sender)

    except Exception as e:
        logger.warning(f'An error occurred: {e}')


@dp.message(F.photo)
async def process_channel_photo(message: Message, bot: Bot):
    sender = message.from_user.username if message.from_user.username else "N/A"
    date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    folder_path = f'{IMAGES_FOLDER}{sender}'
    image_path = f'{folder_path}/{date}.jpg'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    else:
        logger.info(f"Folder already exists: {folder_path}")

    await bot.download(
        message.photo[-1],
        destination=image_path
    )
    logger.info('Photo downloaded!!!')
    date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    extracted_text = im_parser.recognize_text_from_image(image_path, YC_OAUTH, YC_FOLDER_ID)
    saver.save_extracted_text(extracted_text, date, message.from_user.username)

