from datetime import datetime
from itertools import chain
from typing import Any
from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
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


class MagicListAPI(generics.ListAPIView):
    def list(self, request, *args, **kwargs):

        try:
            queryset = self.filter_queryset(self.get_queryset())
            cache_key = f"{request.user} - {queryset.model._meta.model_name}"  # noqa

            page = self.paginate_queryset(queryset)
            cache_response = self.get_cache(cache_key)

            if not cache_response:

                serializer = self.get_serializer(page, many=True)
                cache_response = self.get_cache(cache_key, serializer.data)

            jsonresponse = dict() # noqa
            jsonresponse['code'] = 0
            jsonresponse['msg'] = '操作成功'
            response = self.get_paginated_response(cache_response)
            response._headers['cache-control'] = ('Cache-Control', 'max-age=600')  # noqa
            jsonresponse.update(**response.data)
            response.data = jsonresponse
            return response

        except Exception as err:
            response = ResponseStandard.failed(err)
            return response

    @staticmethod
    def get_cache(cache_key, response=None):
        cache_response = cache.get(cache_key)

        if not cache_response:
            cache.set(cache_key, response)
            cache_response = cache.get(cache_key)

        return cache_response


class MagicDestroyApi(generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(err))


class MagicUpdateApi(generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):

        response = None
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = ResponseStandard.success(data=serializer.data)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(response)


class MagicCreateApi(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ResponseStandard.success(data=serializer.data))
