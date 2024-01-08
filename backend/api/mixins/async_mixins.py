from typing import Dict
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.settings import api_settings


class AsyncCreateModelMixin(CreateModelMixin):
    """Make `create()` and `perform_create()` overridable.

    Without inheriting this class, the event loop can't be used in these two methods when override them.

    This must be inherited before `CreateModelMixin`.

        class MyViewSet(AsyncMixin, GenericViewSet, AsyncCreateModelMixin, CreateModelMixin):
            pass
    """

    async def create(self, request, *args, **kwargs):
        serializer = await self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)  # MODIFIED HERE
        await self.perform_create(serializer)  # MODIFIED HERE
        headers = await self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    async def perform_create(self, serializer):
        await sync_to_async(serializer.save)()

    async def get_success_headers(self, data) -> Dict:
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class AsyncListModelMixin(ListModelMixin):
    async def list(self, request, *args, **kwargs):
        queryset = await self.filter_queryset(await self.get_queryset())
        # queryset = await sync_to_async(queryset)()

        page = await self.paginate_queryset(queryset)
        if page is not None:
            serializer = await self.get_serializer(page, many=True)
            return await self.get_paginated_response(serializer.data)

        serializer = await self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AsyncRetrieveModelMixin(RetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    async def retrieve(self, request, *args, **kwargs):
        instance = await self.get_object()
        serializer = await self.get_serializer(instance)
        return Response(serializer.data)


class AsyncUpdateModelMixin(UpdateModelMixin):
    """
    Update a model instance.
    """

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = await self.get_object()
        serializer = await self.get_serializer(instance, data=request.data, partial=partial)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    async def perform_update(self, serializer):
        await sync_to_async(serializer.save)()

    async def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return await self.update(request, *args, **kwargs)


class AsyncDestroyModelMixin(DestroyModelMixin):
    """Make `destroy()` and `perform_destroy()` overridable.

    Without inheriting this class, the event loop can't be used in these two methods when override them.

    This must be inherited before `DestroyModelMixin`.

        class MyViewSet(AsyncMixin, GenericViewSet, AsyncDestroyModelMixin, DestroyModelMixin):
            pass
    """

    async def destroy(self, request, *args, **kwargs):
        instance = await self.get_object()  # MODIFIED HERE
        await self.perform_destroy(instance)  # MODIFIED HERE
        return Response(status=status.HTTP_204_NO_CONTENT)

    async def perform_destroy(self, instance):
        await sync_to_async(instance.delete)()
