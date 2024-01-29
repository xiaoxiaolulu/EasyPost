import typing
from datetime import datetime
from itertools import chain
from typing import Any
from rest_framework import status
from utils.encoder import jsonable_encoder


class ResponseStandard:

    @staticmethod
    def model_to_dict(instance, fields=None, exclude=None):
        if getattr(instance, '__table__', None) is None:
            return instance
        data = dict()
        opts = instance._meta  # noqa
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if not getattr(f, 'editable', False):
                continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:

                continue
            data[f.name] = f.value_from_object(instance)
        return data

    @staticmethod
    def encode_json(data: Any, *exclude: str):
        return jsonable_encoder(data, exclude=exclude, custom_encoder={
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
        })

    @staticmethod
    def success(data=None, code=0, msg="操作成功✅", exclude=()):
        return ResponseStandard.encode_json(dict(code=code, msg=msg, data=data), *exclude)

    @staticmethod
    def failed(msg="操作失败❌", code=110, data=None):
        return dict(code=code, msg=str(msg), data=data)

    @staticmethod
    def resp_200(*, data: typing.Any = '', msg: str = "Success✅") -> dict:
        return {'code': 200, 'data': data, 'msg': msg}

    @staticmethod
    def resp_400(code: int = 400, data: str = None, msg: str = "请求错误(400)❌") -> dict:
        return dict(status_code=status.HTTP_400_BAD_REQUEST, content={'code': code, 'msg': msg, 'data': data})

    @staticmethod
    def resp_401(*, data: str = None, msg: str = "未授权，请重新登录(401)❌") -> dict:
        return dict(status_code=status.HTTP_401_UNAUTHORIZED, content={'code': 401, 'msg': msg, 'data': data})

    @staticmethod
    def resp_403(*, data: str = None, msg: str = "拒绝访问(403)❌") -> dict:
        return dict(status_code=status.HTTP_403_FORBIDDEN, content={'code': 403, 'msg': msg, 'data': data})

    @staticmethod
    def resp_404(*, data: str = None, msg: str = "请求出错(404)❌") -> dict:
        return dict(status_code=status.HTTP_404_NOT_FOUND, content={'code': 404, 'msg': msg, 'data': data})

    @staticmethod
    def resp_422(*, data: str = None, msg: typing.Union[list, dict, str] = "不可处理的实体❌") -> dict:
        return dict(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'code': 422, 'msg': msg, 'data': data})

    @staticmethod
    def resp_500(*, data: str = None, msg: typing.Union[list, dict, str] = "服务器错误(500)❌") -> dict:
        return dict(headers={'Access-Control-Allow-Origin': '*'},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={'code': 500, 'msg': msg, 'data': data})

    @staticmethod
    def resp_502(*, data: str = None, msg: str = "网络错误(502)❌") -> dict:
        return dict(status_code=status.HTTP_502_BAD_GATEWAY, content={'code': 502, 'msg': msg, 'data': data})

    @staticmethod
    def resp_406(*, data: str = None, msg: str = "请求的格式不可得(406)❌") -> dict:
        return dict(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    content={'code': 406, 'msg': msg, 'data': data})

    @staticmethod
    def resp_408(*, data: str = None, msg: str = "请求超时(408)❌") -> dict:
        return dict(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                    content={'code': 408, 'msg': msg, 'data': data})

    @staticmethod
    def resp_410(*, data: str = None, msg: str = "请求的资源被永久删除，且不会再得到的(410)❌") -> dict:
        return dict(status_code=status.HTTP_410_GONE, content={'code': 410, 'msg': msg, 'data': data})

    @staticmethod
    def resp_501(*, data: str = None, msg: str = "服务未实现(501)❌") -> dict:
        return dict(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    content={'code': 501, 'msg': msg, 'data': data})

    @staticmethod
    def resp_503(*, data: str = None, msg: str = "服务不可用(503)❌") -> dict:
        return dict(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content={'code': 503, 'msg': msg, 'data': data})

    @staticmethod
    def resp_504(*, data: str = None, msg: str = "网络超时(504)❌") -> dict:
        return dict(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    content={'code': 504, 'msg': msg, 'data': data})

    @staticmethod
    def resp_505(*, data: str = None, msg: str = "HTTP版本不受支持(505)❌") -> dict:
        return dict(status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
                    content={'code': 505, 'msg': msg, 'data': data})
