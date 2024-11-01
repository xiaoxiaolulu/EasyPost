import asyncio
import inspect
from asgiref.sync import sync_to_async
from django.db.models import (
    QuerySet,
    Model
)
from rest_framework import exceptions, status
from rest_framework.generics import (
    GenericAPIView,
    get_object_or_404
)
from rest_framework.request import Request
from rest_framework.views import APIView
from api.mixins.async_mixins import (
    AsyncCreateModelMixin,
    AsyncListModelMixin,
    AsyncRetrieveModelMixin,
    AsyncDestroyModelMixin,
    AsyncUpdateModelMixin
)


class AsyncAPIView(APIView):
    """
    Provides async view compatible support for DRF Views and ViewSets.

    This must be the first inherited class.
    """

    @classmethod
    def as_view(cls, *args, **initkwargs): # noqa
        """Make Django process the view as an async view."""
        view = super().as_view(*args, **initkwargs) # noqa

        async def async_view(*args, **kwargs): # noqa
            # wait for the `dispatch` method
            return await view(*args, **kwargs)

        async_view.cls = cls
        async_view.initkwargs = initkwargs # noqa
        async_view.csrf_exempt = True
        return async_view

    async def get_exception_handler_context(self):
        # 返回异常上下文
        return await sync_to_async(super().get_exception_handler_context)()

    async def get_exception_handler(self):
        # 不论异常函数是不是协程
        return super().get_exception_handler()

    async def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = await sync_to_async(self.get_authenticate_header)(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = await self.get_exception_handler()

        context = await self.get_exception_handler_context()

        # 如果自定义异常函数不是协程
        if not asyncio.iscoroutinefunction(exception_handler):
            response = await sync_to_async(exception_handler)(exc, context)
        else:
            response = await exception_handler(exc, context)

        if response is None:
            await sync_to_async(self.raise_uncaught_exception)(exc)

        response.exception = True
        return response

    async def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial process object.
        """
        parser_context = self.get_parser_context(request)

        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context,
        )

    async def dispatch(self, request, *args, **kwargs):
        """Add async support."""
        self.args = args # noqa
        self.kwargs = kwargs # noqa
        request = await self.initialize_request(request, *args, **kwargs)
        self.request = request # noqa
        self.headers = self.default_response_headers # noqa

        try:
            await sync_to_async(self.initial)(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # accept both async and sync handlers
            # built-in handlers are sync handlers
            if not asyncio.iscoroutinefunction(handler):
                handler = sync_to_async(handler)
            response = await handler(request, *args, **kwargs)

        except Exception as exc:
            response = await self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs) # noqa
        return self.response


class AsyncGenericAPIView(
    AsyncAPIView,
    GenericAPIView
):
    async def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return await self.paginator.paginate_queryset(queryset, self.request, view=self)

    async def get_queryset(self) -> QuerySet:
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        query sets depending on the incoming process.

        (E.g. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method. 🦯" % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each process.
            queryset = queryset.all()
        return queryset

    async def get_object(self) -> Model:
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = await self.filter_queryset(await self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly. 🦯" % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = await sync_to_async(get_object_or_404)(queryset, **filter_kwargs)
        obj = await obj
        # May raise a permission denied
        await sync_to_async(self.check_object_permissions)(self.request, obj)

        return obj

    async def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if inspect.iscoroutinefunction(self.get_serializer_class):
            serializer_class = await self.get_serializer_class()
        else:
            serializer_class = await sync_to_async(self.get_serializer_class)()
        kwargs.setdefault("context", await sync_to_async(self.get_serializer_context)())
        return await sync_to_async(serializer_class)(*args, **kwargs)

    async def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming process.

        (E.g. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method. 🦯" % self.__class__.__name__
        )

        return self.serializer_class

    async def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return await self.paginator.get_paginated_response(data)

    async def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter unit-backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering unit-backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = await backend().filter_queryset(self.request, queryset, self)
        if inspect.iscoroutine(queryset):
            return await queryset
        return queryset


# Concrete view classes that provide method handlers
# by composing the mixin classes with the base view.


class AsyncCreateAPIView(
    AsyncCreateModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for creating a model instance.
    """

    async def post(self, request, *args, **kwargs):
        return await self.create(request, *args, **kwargs)


class AsyncListAPIView(AsyncListModelMixin, AsyncGenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    async def get(self, request, *args, **kwargs):
        return await self.list(request, *args, **kwargs)


class AsyncRetrieveAPIView(
    AsyncRetrieveModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for retrieving a model instance.
    """

    async def get(self, request, *args, **kwargs):
        return await self.retrieve(request, *args, **kwargs)


class AsyncDestroyAPIView(
    AsyncDestroyModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for deleting a model instance.
    """

    async def delete(self, request, *args, **kwargs):
        return await self.destroy(request, *args, **kwargs)


class AsyncUpdateAPIView(
    AsyncUpdateModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for updating a model instance.
    """

    async def put(self, request, *args, **kwargs):
        return await self.update(request, *args, **kwargs)

    async def patch(self, request, *args, **kwargs):
        return await self.partial_update(request, *args, **kwargs)


class AsyncListCreateAPIView(
    AsyncListModelMixin,
    AsyncCreateModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    async def get(self, request, *args, **kwargs):
        return await self.list(request, *args, **kwargs)

    async def post(self, request, *args, **kwargs):
        return await self.create(request, *args, **kwargs)


class AsyncRetrieveUpdateAPIView(
    AsyncRetrieveModelMixin,
    AsyncUpdateModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for retrieving, updating a model instance.
    """

    async def get(self, request, *args, **kwargs):
        return await self.retrieve(request, *args, **kwargs)

    async def put(self, request, *args, **kwargs):
        return await self.update(request, *args, **kwargs)

    async def patch(self, request, *args, **kwargs):
        return await self.partial_update(request, *args, **kwargs)


class AsyncRetrieveDestroyAPIView(
    AsyncRetrieveModelMixin,
    AsyncDestroyModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    async def get(self, request, *args, **kwargs):
        return await self.retrieve(request, *args, **kwargs)

    async def delete(self, request, *args, **kwargs):
        return await self.destroy(request, *args, **kwargs)


class AsyncRetrieveUpdateDestroyAPIView(
    AsyncRetrieveModelMixin,
    AsyncUpdateModelMixin,
    AsyncDestroyModelMixin,
    AsyncGenericAPIView
):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    async def get(self, request, *args, **kwargs):
        return await self.retrieve(request, *args, **kwargs)

    async def put(self, request, *args, **kwargs):
        return await self.update(request, *args, **kwargs)

    async def patch(self, request, *args, **kwargs):
        return await self.partial_update(request, *args, **kwargs)

    async def delete(self, request, *args, **kwargs):
        return await self.destroy(request, *args, **kwargs)
