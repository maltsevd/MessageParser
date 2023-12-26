import os
import base64
import json
from requests import post
from loguru import logger


class ImageParser:
    """
    Handles image recognition and text extraction using Yandex Cloud OCR services.

    This class facilitates obtaining IAM tokens, sending image data for analysis,
    and extracting text from the analyzed image using Yandex OCR API.

    Methods:
        _get_iam_token(iam_url, oauth_token): Retrieve IAM token for Yandex account.
        _request_analyze(vision_url, iam_token, folder_id, image_data): Send image for OCR analysis.
        _list_files(directory): List files in a specified directory.
        _extract_text(json_obj, target_key): Extract text by searching JSON object for a target key.
        recognize_text_from_image(image_path, yc_oauth, yc_folder_id): Perform OCR on an image and extract text.
    """

    def _get_iam_token(self, iam_url, oauth_token):
        """
        Retrieve IAM token for Yandex account.

        Parameters:
            iam_url (str): URL for obtaining the IAM token.
            oauth_token (str): OAuth token for authentication.

        Returns:
            str or None: IAM token if successful, else None.
        """
        response = post(iam_url, json={"yandexPassportOauthToken": oauth_token}, timeout=30)
        json_data = json.loads(response.text)

        if json_data is not None and 'iamToken' in json_data:
            logger.info('IAM token obtained')
            return json_data['iamToken']
        return None

    def _request_analyze(self, vision_url, iam_token, folder_id, image_data):
        """
        Send image for OCR analysis and return server's response.

        Parameters:
            vision_url (str): URL of the vision API.
            iam_token (str): IAM token for authentication.
            folder_id (str): Folder ID for Yandex Cloud.
            image_data (str): Base64 encoded image data.

        Returns:
            dict: JSON response from the server.
        """
        response = post(vision_url, headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + iam_token,
                                             'x-folder-id': folder_id,
                                             'x-data-logging-enabled': 'true'},
                        json={"mimeType": "JPEG",
                              "languageCodes": ["*"],
                              "model": "page",
                              "content": image_data}, timeout=30)
        logger.info('JSON obtained')
        return response.json()

    def _list_files(self, directory):
        """
        List files in a specified directory.

        Parameters:
            directory (str): Path to the directory.

        Returns:
            list: File names in the directory.
        """
        return list(os.listdir(directory))

    def _extract_text(self, json_obj, target_key):
        """
        Extract text by searching a JSON object for a target key.

        Parameters:
            json_obj (dict or list): JSON object to search.
            target_key (str): Key to search for.

        Returns:
            Value associated with the target key, or None if not found.
        """
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                if key == target_key:
                    return value
                if isinstance(value, (dict, list)):
                    result = self._extract_text(value, target_key)
                    if result is not None:
                        return result
        return None

    def recognize_text_from_image(self, image_path, yc_oauth, yc_folder_id):
        """
        Perform OCR on an image and extract text.

        Parameters:
            image_path (str): File path of the image.
            yc_oauth (str): OAuth token for Yandex Cloud.
            yc_folder_id (str): Folder ID in Yandex Cloud.

        Returns:
            str or None: Extracted text, or None if extraction fails.
        """
        iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
        vision_url = 'https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText'
        iam_token = self._get_iam_token(iam_url, yc_oauth)

        try:
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response = self._request_analyze(vision_url, iam_token, yc_folder_id, image_data)
            extracted_text = self._extract_text(response, 'fullText')
            logger.info('Text extracted')
            return extracted_text
        except RuntimeError as e:
            logger.warning(f'Text not extracted. Error: {e}')
        return None
