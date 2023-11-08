from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db import DatabaseError
from redis.exceptions import RedisError
import traceback
from rest_framework.views import set_rollback
from api.response.fatcory import ResponseStandard


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文（包含request请求对象和view视图对象）
    :return: Response响应对象
    """
    def inner_exception_handler(inner_exc, inner_context):
        if isinstance(inner_exc, Http404):
            inner_exc = exceptions.NotFound()
        elif isinstance(inner_exc, PermissionDenied):
            inner_exc = exceptions.PermissionDenied()

        if isinstance(inner_exc, exceptions.APIException):
            headers = {}
            if getattr(inner_exc, 'auth_header', None):
                headers['WWW-Authenticate'] = inner_exc.auth_header # noqa
            if getattr(inner_exc, 'wait', None):
                headers['Retry-After'] = '%d' % inner_exc.wait  # noqa

            if isinstance(inner_exc.detail, dict):
                data = inner_exc.detail
                data = "".join([f"{key} {value}" for key, value in data.items()])
            else:
                data = inner_exc.detail

            set_rollback()
            # 捕获401鉴权失败，直接返回 11000
            if inner_exc.status_code == 401:
                return Response(ResponseStandard.failed(msg=data, code=11000))
            else:
                return Response(ResponseStandard.failed(msg=data))

        return None

    response = inner_exception_handler(exc, context)
    if response is not None:
        return response

    # 捕获其他异常，直接返回 500
    if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
        return Response(ResponseStandard.failed(f'其他未知错误：{traceback.format_exc()}'))
    else:
        return Response(ResponseStandard.failed(f'其他未知错误：{traceback.format_exc()}'))


def jwt_response_payload_error_handler(serializer, request=None):

    data = "".join([f"{key} {value}" for key, value in serializer.errors.items()])
    return Response(
        ResponseStandard.failed(msg=data)
    )
