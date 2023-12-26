import os
from app import IMAGES_FOLDER, YC_RESPONSE_FOLDER, YC_EXTRACTED_TEXTS, TG_MESSAGES_FOLDER
from loguru import logger
import json
import csv


def _check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Folder created: {path}")
    else:
        logger.info(f"Folder already exists: {path}")


def save_json(file, filename, username):
    path = f'{YC_RESPONSE_FOLDER}{username}'
    _check_path(path)
    try:
        with open(f'{path}/{filename}.json', "w") as outfile:
            json.dump(file, outfile)
            logger.info('JSON saved')
    except Exception as e:
        logger.warning(f'JSON not saved! Error: {e}')


def save_image(image, filename, username):
    path = f'{IMAGES_FOLDER}{username}'
    _check_path(path)
    try:
        with open(f'{path}/{filename}', "w") as outfile:
            json.dump(image, outfile)
            logger.info('Image saved')
    except Exception as e:
        logger.warning(f'Image not saved! Error: {e}')


def save_extracted_text(text, filename, username):
    path = f'{YC_EXTRACTED_TEXTS}{username}'
    _check_path(path)
    try:
        with open(f'{path}/{filename}.txt', "w") as outfile:
            outfile.write(text)
            logger.info('Extracted text saved')
    except Exception as e:
        logger.warning(f'Extracted text not saved! Error: {e}')


def save_message(message, date, username):
    path = f'{TG_MESSAGES_FOLDER}{username}'
    _check_path(path)
    try:
        # Append the message data to the CSV file
        with open(f'{path}/messages.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([date, username, message])
            logger.info(f'Message saved')
    except Exception as e:
        logger.warning(f'TG message not saved! Error: {e}')

