import requests
from utils.logger import logger


class Webhook:
    """
    This class provides a wrapper for sending data to a webhook URL.

    It sends a POST request with the provided data in JSON format.
    """

    def __init__(self, base_url: str, data: dict):
        """
        Initializes a Webhook object.

        Args:
            base_url (str): The URL of the webhook endpoint.
            data (dict): The data to be sent in the request body (JSON format).
        """
        self.base_url = base_url
        self.data = data

    def send(self) -> None:
        """
        Sends data to the specified webhook URL using a POST request.

        Handles exceptions and logs success/failure messages.
        """
        try:
            response = requests.post(
                url=self.base_url,
                json=self.data
            )
            response.raise_for_status()  # Raise exception for non-2xx status codes
        except requests.exceptions.RequestException as e:  # Catch specific request exceptions
            logger.error(f'Webhook request failed: {e}')
        else:
            logger.success('Webhook message sent successfully')
