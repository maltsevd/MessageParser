# Message Parser
This project includes a Telegram bot that uses the Yandex Cloud OCR services for image recognition and text extraction.

## Description

The bot is designed to process messages and images sent to it on Telegram, extracting text from images using Yandex Cloud's OCR capabilities. The main components of the project are:

1. `ImageParser`: A class responsible for handling the OCR process. It communicates with the Yandex Cloud services to recognize text from images.

2. `TelegramParser`: A class that initializes and runs the Telegram bot, handling incoming messages and images.

3. Main script: The entry point of the application that initializes the `TelegramParser` and starts the bot.

## Getting Started

### Dependencies

- Python 3.x
- `aiogram` for Telegram bot integration
- `requests` for making HTTP requests to Yandex Cloud
- `loguru` for logging
- `asyncio` for asynchronous programming

### Installing

- Clone the repository
- Install the necessary packages using `pip install -r requirements.txt` or with poetry using `poetry init` in the project folder.

### Executing program

- Start the bot by running bash-script:
```
bash run_parser.sh
```
  
## Authors

Danila M.
