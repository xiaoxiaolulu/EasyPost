import asyncio
import functools
import os
import typing
from typing import (
    Callable,
    TypeVar,
    Optional,
    Awaitable
)
import anyio
from redlock import (
    RedLock,
    RedLockError
)
from config import settings


def lock(key):
    """
    redis分布式锁，基于redlock
    :param key: 唯一key，确保所有任务一致，但不与其他任务冲突
    :return:
    """

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}",
                                 connection_details=settings.REDIS_NODES,
                                 ttl=30000,  # 锁释放时间为30s
                                 ):
                        return await func(*args, **kwargs)
                except RedLockError:
                    print(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}",
                                 connection_details=settings.REDIS_NODES,
                                 ttl=30000,  # 锁释放时间为30s
                                 ):
                        return func(*args, **kwargs)
                except RedLockError:
                    print(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")
        return wrapper

    return decorator


T_ParamSpec = TypeVar("T_ParamSpec", bound=Callable)
T_Retval = TypeVar("T_Retval")


def sync_to_async(
    function: Callable[[T_ParamSpec], T_Retval],
    *,
    cancellable: bool = False,
    limiter: Optional[anyio.CapacityLimiter] = None,
) -> Callable[[T_ParamSpec], Awaitable[T_Retval]]:
    """
    Converts a synchronous function into an asynchronous one using anyio.

    Args:
        function: The synchronous function to asyncify.
        cancellable: Whether to allow cancellation of the task. Defaults to False.
        limiter: Optional capacity limiter for concurrency control.

    Returns:
        An asynchronous wrapper function.
    """

    async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> T_Retval:
        """Async wrapper that calls the synchronous function in a thread pool."""
        task = anyio.to_thread.run_sync(
            functools.partial(function, *args, **kwargs),
            cancellable=cancellable,
            limiter=limiter,
        )
        return await task

    return wrapper


def async_to_sync(
    function: Callable[..., Awaitable[T_Retval]],
) -> Callable[..., T_Retval]:
    """
    Converts an asynchronous function into a synchronous one using anyio.

    Args:
        function: The asynchronous function to syncify.

    Returns:
        A synchronous wrapper function.
    """

    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> T_Retval:
        """Synchronous wrapper that calls the asynchronous function."""
        task = anyio.run(function, *args, **kwargs)  # noqa
        return task

    return wrapper
