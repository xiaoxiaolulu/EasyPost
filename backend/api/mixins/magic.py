from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
from api.response.fatcory import ResponseStandard


class MagicListAPI(generics.ListAPIView):
    def list(self, request, *args, **kwargs):

        try:
            queryset = self.filter_queryset(self.get_queryset())

            # get cache
            cache_key = f"{request.user} - {queryset.model._meta.model_name}"  # noqa
            cache_response = self.get_cache(cache_key)

            if not cache_response:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)
                response = self.set_catch(cache_key, serializer.data)
            else:
                response = cache_response

            return Response(ResponseStandard.success(response))

        except Exception as err:
            response = ResponseStandard.failed(err)
            return Response(response)

    @staticmethod
    def get_cache(cache_key):
        cache_response = cache.get(cache_key)

        return cache_response

    @staticmethod
    def set_catch(cache_key, response):
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
            self.perform_update(serializer)
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
