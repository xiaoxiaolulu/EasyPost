import typing
from enum import Enum

Name = str
Url = str
Headers = typing.Dict[str, str]


class MethodEnum(str, Enum):
    """请求方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    NA = "N/A"
