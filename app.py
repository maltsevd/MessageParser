import os
from dotenv import load_dotenv

load_dotenv()

YC_OAUTH = os.getenv('YC_OAUTH')
YC_FOLDER_ID = os.getenv('YC_FOLDER_ID')
IMAGES_FOLDER = os.getenv('IMAGES_FOLDER')
YC_RESPONSE_FOLDER = os.getenv('YC_RESPONSE_FOLDER')
YC_EXTRACTED_TEXTS = os.getenv('YC_EXTRACTED_TEXTS')
TG_MESSAGES_FOLDER = os.getenv('TG_MESSAGES_FOLDER')
BOT_TOKEN = os.getenv('BOT_TOKEN')

