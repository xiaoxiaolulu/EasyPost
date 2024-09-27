from grpc_interceptor.server import AsyncServerInterceptor
import grpc
from typing import (
    Any,
    Callable
)
from grpc_interceptor.exceptions import GrpcException


class ExecutorInterceptor(AsyncServerInterceptor):
    async def intercept(
            self,
            method: Callable,
            request_or_iterator: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        try:
            response = await method(request_or_iterator, context)
            return response
        except GrpcException as e:
            await context.set_code(e.status_code)
            await context.set_details(e.details)
