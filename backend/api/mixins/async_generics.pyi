import asyncio
from asgiref.sync import sync_to_async
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.views import APIView


class AsyncAPIView(APIView):
    """
    Provides async view compatible support for DRF Views and ViewSets.

    This must be the first inherited class.
    """

    @classmethod
    def as_view(cls, *args, **initkwargs):
        """Make Django process the view as an async view."""
        view = super().as_view(*args, **initkwargs)

        async def async_view(*args, **kwargs):
            # wait for the `dispatch` method
            return await view(*args, **kwargs)

        async_view.cls = cls
        async_view.initkwargs = initkwargs
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
        Returns the initial request object.
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
        self.args = args
        self.kwargs = kwargs
        request = await self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

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

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
