from datetime import datetime
from itertools import chain
from typing import Any
from django.core.cache import cache
from rest_framework import generics
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
    def success(data=None, code=0, msg="操作成功", exclude=()):
        return ResponseStandard.encode_json(dict(code=code, msg=msg, data=data), *exclude)

    @staticmethod
    def failed(msg, code=110, data=None):
        return dict(code=code, msg=str(msg), data=data)


class ListAPI(generics.ListAPIView):
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        cache_key = f"{request.user} - {queryset.model._meta.model_name}"  # noqa

        page = self.paginate_queryset(queryset)
        cache_response = self.get_cache(cache_key)

        if not cache_response:

            serializer = self.get_serializer(page, many=True)
            cache_response = self.get_cache(cache_key, serializer.data)

        response = self.get_paginated_response(cache_response)
        response._headers['cache-control'] = ('Cache-Control', 'max-age=600')  # noqa
        return response

    @staticmethod
    def get_cache(cache_key, response=None):
        cache_response = cache.get(cache_key)

        if not cache_response:
            cache.set(cache_key, response)
            cache_response = cache.get(cache_key)

        return cache_response
