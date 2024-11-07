import base64
import hashlib
import hmac
import time
import urllib.parse
import requests
from api.events.registry import registry


@registry.register("DINGDING")
class DingTalk:
    """
    This class provides a wrapper for sending notifications to DingTalk groups.

    It can handle signing requests for added security when a secret is provided.
    """

    def __init__(self, url, data, secret=None):
        """
        Initializes a DingTalk object.

        Args:
            url (str): The URL of the DingTalk notification endpoint.
            data (dict): The data to be sent in the process body (usually JSON format).
            secret (str, optional): The secret key for signing requests. Defaults to None.
        """
        self.url = url
        self.data = data
        self.secret = secret

    def get_stamp(self):
        """
        Generates a timestamp and signature for secure DingTalk API requests.

        This method is used when a secret key is provided for signing.

        Returns:
            dict: A dictionary containing the timestamp and signature.
        """
        timestamp = str(round(time.time() * 1000))  # Milliseconds since epoch
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f"{timestamp}\n{self.secret}"  # Combine timestamp and secret
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {"sign": sign, "timestamp": timestamp}

    def send_info(self):
        """
        Sends data to the specified DingTalk notification endpoint.

        Automatically adds signing parameters if a secret is provided.

        Args:
            None

        Returns:
            requests.Response: The response object from the API call.

        Raises:
            requests.exceptions.RequestException: If the API process fails.
        """
        if self.secret:
            params = self.get_stamp()
        else:
            params = None
        response = requests.post(url=self.url, json=self.data, params=params)
        return response
