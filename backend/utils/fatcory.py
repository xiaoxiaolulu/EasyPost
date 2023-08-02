from datetime import datetime
from itertools import chain
from typing import Any
from utils.encoder import jsonable_encoder


class ResponseStandard:

    @staticmethod
    def model_to_dict(instance, fields=None, exclude=None):
        if getattr(instance, '__table__', None) is None:
            return instance
        data = dict()
        opts = instance._meta
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
    def success(data=None, code=0, msg="操作成功", exclude=()):
        return ResponseStandard.encode_json(dict(code=code, msg=msg, data=data), *exclude)
