import os
from requests import post
import json
import base64
from loguru import logger


class ImageParser:
    def _get_iam_token(self, iam_url, oauth_token):
        """
        The function returns the IAM token for the Yandex account.
        :param iam_url:
        :param oauth_token:
        :return: token string
        """
        response = post(iam_url, json={"yandexPassportOauthToken": oauth_token})
        json_data = json.loads(response.text)

        if json_data is not None and 'iamToken' in json_data:
            logger.info('IAM token obtained')
            return json_data['iamToken']
        return None

    def _request_analyze(self, vision_url, iam_token, folder_id, image_data):
        """
        The function sends an image recognition request to the server and returns a response from the  server.
        :param vision_url:
        :param iam_token:
        :param folder_id:
        :param image_data:
        :return: content of response
        """
        response = post(vision_url, headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer '+iam_token,
                                             'x-folder-id': folder_id,
                                             'x-data-logging-enabled': 'true'}, json={"mimeType": "JPEG",
                                                                                      "languageCodes": ["*"],
                                                                                      "model": "page",
                                                                                      "content": image_data
                                                                                      })
        logger.info('JSON obtained')
        return response.json()


    def _list_files(self, directory):
        """
        List all files in a given directory.

        :param directory: The path to the directory to list files from.
        :return: A list of file names.
        """
        return [file for file in os.listdir(directory)]

    def _extract_text(self, json_obj, target_key):
        """
        Recursively search for a target key in a JSON object.

        :param json_obj: The JSON object (dict or list) to search in.
        :param target_key: The key to search for.
        :return: The value associated with the target key, or None if the key is not found.
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
        iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
        vision_url = 'https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText'
        iam_token = self._get_iam_token(iam_url, yc_oauth)

        try:
            with open(f'{image_path}', "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response = self._request_analyze(vision_url, iam_token, yc_folder_id, image_data)
            extracted_text = self._extract_text(response, 'fullText')
            logger.info('Text extracted')
            return extracted_text
        except Exception as e:
            logger.warning(f'Text not extracted. Error: {e}')
        return None

