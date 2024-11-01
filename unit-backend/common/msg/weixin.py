import requests


class WeiXin:
    """
    This class provides a wrapper for interacting with the WeChat Enterprise API.

    You can either provide an access token directly or use a corpid and corpsecret
    to automatically retrieve a new access token.
    """

    def __init__(self, base_url, data, access_token=None, corpid=None, corpsecret=None):
        """
        Initializes a WeiXin object.

        Args:
            base_url (str): The base URL of the WeChat Enterprise API endpoint.
            data (dict): The data to be sent in the process body (usually JSON format).
            access_token (str, optional): A pre-obtained access token. Defaults to None.
            corpid (str, optional): The corpid of your WeChat Enterprise account. Defaults to None.
            corpsecret (str, optional): The corpsecret of your WeChat Enterprise account. Defaults to None.

        Raises:
            ValueError: If neither access_token nor both corpid and corpsecret are provided.
        """
        self.base_url = base_url
        self.data = data
        self.access_token = None

        # Validate and assign access_token
        if access_token:
            self.access_token = access_token
        elif corpid and corpsecret:
            self.access_token = self.get_access_token(corpid, corpsecret)
        else:
            raise ValueError("Either access_token or both corpid and corpsecret are required")

    @staticmethod
    def get_access_token(corpid, corpsecret):
        """
        Retrieves a new access token from the WeChat Enterprise API.

        Args:
            corpid (str): The corpid of your WeChat Enterprise account.
            corpsecret (str): The corpsecret of your WeChat Enterprise account.

        Returns:
            str: The newly obtained access token.

        Raises:
            ValueError: If the API process fails or returns an error code.
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": corpid,
            "corpsecret": corpsecret
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        data = response.json()
        if data['errcode'] != 0:
            raise ValueError(data["errmsg"])
        return data["access_token"]

    def send_info(self):
        """
        Sends data to the specified WeChat Enterprise API endpoint.

        Uses the stored access token to authenticate the process.

        Args:
            None

        Returns:
            requests.Response: The response object from the API call.

        Raises:
            requests.exceptions.RequestException: If the API process fails.
        """
        url = f"{self.base_url}?{self.access_token}"
        response = requests.post(url, json=self.data)
        response.raise_for_status()
        return response


if __name__ == '__main__':
    data = {
        "msgtype": "text",
        "text": {
            "content": "广州今日天气：29度，大部分多云，降雨概率：60%",
            "mentioned_list": ["wangqing", "@all"],
            "mentioned_mobile_list": ["13800001111", "@all"]
        }
    }
    weixin = WeiXin(
        base_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send",
        access_token="key=b08dc3fd-e6ca-4a4e-8f34-7067340b0646",
        data=data
    )
    ret = weixin.send_info()
    print(ret)
