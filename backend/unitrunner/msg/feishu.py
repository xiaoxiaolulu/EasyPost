import requests
from utils.logger import logger


class FeiShu:
    """
    This class provides a wrapper for sending messages to FeiShu.

    It constructs a message payload in the specified format and sends it to the provided URL.
    """

    def __init__(self, base_url: str, content: dict):
        """
        Initializes a FeiShu object.

        Args:
            base_url (str): The URL of the FeiShu message endpoint.
            content (dict): A dictionary containing the message content.
        """
        self.base_url = base_url
        self.content = content

    def send(self) -> None:
        """
        Sends a FeiShu message using the provided content.

        Handles exceptions and logs success/failure messages.

        Args:
            None
        """
        # Construct message payload in FeiShu's specified format
        data = {
            'msg_type': 'post',
            'content': {
                'post': {
                    'zh_cn': {
                        'title': "自动化测试报告",
                        'content': [
                            [{'tag': 'text', 'text': f" 测试人员: {self.content['user']}"}],
                            [{'tag': 'text', 'text': f" 测试结果: {self.content['result']}"}],
                            [{'tag': 'text', 'text': f"✅ 通过用例: {self.content['passed']}"}],
                            [{'tag': 'text', 'text': f" 失败用例: {self.content['failed']}"}],
                            [{'tag': 'text', 'text': f"❌ 错误用例: {self.content['error']}"}],
                            [{'tag': 'text', 'text': f"⚠️ 跳过用例: {self.content['skipped']}"}],
                            [{'tag': 'text', 'text': f"⌛ 开始时间: {self.content['started_time']}"}],
                            [{'tag': 'text', 'text': f"⏱️ 执行耗时: {self.content['elapsed']}"}],
                            [{'tag': 'a', 'text': '➡️ 查看详情', 'href': 'https://foryourself'}],
                        ],
                    }
                }
            }
        }

        try:
            # Send the message using requests
            response = requests.session().post(
                url=self.base_url,
                json=data
            )
            response.raise_for_status()  # Raise exception for non-2xx status codes
        except Exception as e:
            # Log error message using the provided logger
            logger.error(f'飞书消息发送异常: {e}')
        else:
            # Log success message using the provided logger
            logger.success('飞书消息发送成功')
