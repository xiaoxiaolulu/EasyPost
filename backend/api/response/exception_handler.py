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
    def inner_exception_handler(ex, con):
        if isinstance(ex, Http404):
            ex = exceptions.NotFound()
        elif isinstance(ex, PermissionDenied):
            ex = exceptions.PermissionDenied()

        if isinstance(ex, exceptions.APIException):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait

            if isinstance(exc.detail, (list, dict)):
                data = exc.detail
                data = "".join([f"{key} {value}" for key, value in data.items()])
            else:
                data = {'detail': exc.detail}

            set_rollback()
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
