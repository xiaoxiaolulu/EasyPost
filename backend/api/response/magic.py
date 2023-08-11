from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
from api.response.fatcory import ResponseStandard


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


class MagicRetrieveApi(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(ResponseStandard.success(data=serializer.data))