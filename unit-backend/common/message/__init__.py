from api.events.registry import registry
from common.message.dingtalk import DingTalk
from common.message.feishu import FeiShu
from common.message.webhook import Webhook
from common.message.weixin import WeiXin
from utils.logger import logger


def message_runner(msg_type, url, data):
    """
    Sends a message based on the specified message type.

    Args:
        msg_type: The type of message to send (e.g., NoticeType.WEBHOOK).
        url: The URL to send the message to.
        data: The data to be sent with the message.
    """

    message_class = registry.get(msg_type, None)
    if message_class:
        message_object = message_class(url, data)
        message_object.send_info()
    else:
        logger.warning(f"Invalid message type: {msg_type}")
