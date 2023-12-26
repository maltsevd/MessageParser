import os
from aiogram import F, Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from loguru import logger
from src.parsers import ImageParser
from src.utils import saver
from app import BOT_TOKEN, YC_OAUTH, IMAGES_FOLDER, YC_FOLDER_ID

# Initialize an image parser object
im_parser = ImageParser()

# Setup logging to file
logger.add("logs/logs_from_tg_bot.log", level="INFO")

# Initialize the bot with the provided token and set parse mode to HTML
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
logger.info("Initialized Bot")

# Initialize dispatcher for the bot to manage incoming updates and registered handlers
dp = Dispatcher()


@dp.message(F.text)
async def process_channel_messages(message: Message):
    """
    Process text messages from a channel.

    Parameters
    ----------
    message : Message
        The message object received from Telegram.

    Returns
    -------
    None
    """
    try:
        # Extract relevant information from the message
        message_text = message.text
        date = message.date.strftime("%Y-%m-%d %H:%M:%S")
        # Use the sender's username if available, else mark as 'N/A'
        sender = message.from_user.username if message.from_user.username else "N/A"

        # Save the extracted message information
        saver.save_message(message_text, date, sender)

    except RuntimeError as e:
        # Log any exceptions that occur
        logger.warning(f'An error occurred: {e}')


@dp.message(F.photo)
async def process_channel_photo(message: Message, bot: Bot):
    """
    Process photo messages from a channel.

    Parameters
    ----------
    message : Message
        The message object containing the photo received from Telegram.
    bot : Bot
        The bot instance to use for downloading the photo.

    Returns
    -------
    None
    """
    try:
        sender = message.from_user.username if message.from_user.username else "N/A"
        date = message.date.strftime("%Y-%m-%d %H:%M:%S")

        # Define folder and image paths for saving the photo
        folder_path = f'{IMAGES_FOLDER}{sender}'
        image_path = f'{folder_path}/{date}.jpg'

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Folder created: {folder_path}")
        else:
            logger.info(f"Folder already exists: {folder_path}")

        # Download the photo using the bot instance
        await bot.download(
            message.photo[-1],
            destination=image_path
        )
        logger.info('Photo downloaded!!!')

        # Extract text from the downloaded image
        extracted_text = im_parser.recognize_text_from_image(image_path, YC_OAUTH, YC_FOLDER_ID)

        # Save the extracted text along with other information
        saver.save_extracted_text(extracted_text, date, message.from_user.username)

    except RuntimeError as e:
        # Log any exceptions that occur
        logger.warning(f'An error occurred: {e}')
