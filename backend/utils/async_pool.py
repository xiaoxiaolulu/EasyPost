"""Custom Celery worker pool."""

# Future Imports
from __future__ import annotations

# Standard Library Imports
import asyncio as aio
import inspect
import os
import sys
import threading
import time
import typing
from typing import (
    Any,
    Callable,
    Optional,
    Union,
)

# Third-Party Imports
import celery.concurrency.base
import celery.concurrency.solo
import celery.signals
from billiard.einfo import ExceptionInfo
from billiard.exceptions import WorkerLostError
from celery.exceptions import (
    WorkerShutdown,
    WorkerTerminate,
    reraise,
)


# Package-Level Imports
AnyCallable = typing.Callable[..., typing.Any]
AnyException = typing.Union[Exception, typing.Type[Exception]]
AnyCoroutine = typing.Coroutine[typing.Any, typing.Any, typing.Any]


__all__ = ("AsyncIOPool",)


WorkerPoolInfo = dict[
    str,
    Optional[
        Union[
            int,
            bool,
            tuple[int, ...],
            aio.AbstractEventLoop,
        ]
    ],
]


class AsyncIOPool(celery.concurrency.solo.TaskPool):
    """Custom asyncio Celery worker pool class."""

    loop: aio.AbstractEventLoop
    loop_runner: threading.Thread
    singleton: Optional["AsyncIOPool"] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "AsyncIOPool":

        # Because the worker pool uses an instance-bound thread
        # to run its asyncio eventloop, it's a good idea to ensure
        # that there can't be more than one instance of the pool
        # created per process

        if not isinstance(cls.singleton, cls):
            # Package-Level Imports
            from utils.celery_tracer import patch_celery_tracer
            # We can't assume that a user has elected to enable
            # automatic patching of Celery's default `build_tracer`
            # utility. We need to be *guarantee* that the patch
            # has been applied though, and the patching process
            # itself is idempotent therefore safe to call any
            # number of times.
            assert patch_celery_tracer()

            # Create the requested new worker pool and use it to
            # populate the class's currently "empty" `singleton`
            # attribute
            cls.singleton = super(AsyncIOPool, cls).__new__(cls)

        # Return the class-bound worker pool instance
        return cls.singleton

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        # If there is already a running asyncio event loop
        # in the current thread / process, it's not a great
        # idea to allow the worker pool to create another
        # and the `AsyncIOPool` can't function at all without
        # one, so we'll throw a `SystemError` if one is detected
        # as a way to short-circuit the worker start up process
        try:
            aio.get_running_loop()
            raise SystemError("There is already a running event loop in this thread!")
        except RuntimeError:
            pass

        # Regardless of what the user specifies in the local
        # configuration, `threads` and `forking_enable` should
        # *always* be False when using `AsyncIOPool` as the
        # worker pool class, so we'll set them forcibly here

        kwargs.update(
            threads=False,
            forking_enable=False,
        )

        # Call the default constructor method ...
        celery.concurrency.base.BasePool.__init__(
            self,
            *args,
            **kwargs,
        )

        # ... perform the usual "housekeeping", ...
        self.limit = 1
        celery.signals.worker_process_init.send(sender=None)

        # ... create the pool's asyncio eventloop ...
        self.loop = aio.new_event_loop()

        # ... and let it run in an instance-bound thread.
        self.loop_runner = threading.Thread(
            target=self.loop.run_forever,
            name="celery-worker-async-loop",
            daemon=True,
        )

        self.loop_runner.start()

        # Set the new event loop as the "active" eventloop
        # in current thread / process
        aio.set_event_loop(self.loop)

    def _get_info(self) -> WorkerPoolInfo:
        info = super()._get_info()
        info.update({
            "timeouts": (),
            "max-concurrency": 1,
            "event-loop": str(self.loop),
            "max-tasks-per-child": None,
            "processes": (os.getpid(),),
            "put-guarded-by-semaphore": True,
        })
        return info

    def run(
        self,
        task_function: AnyCallable | AnyCoroutine,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run the supplied coroutine in the pool's bound loop-runner
        thread."""

        # If the supplied function is actually an async function
        # (i.e. async def some_function() -> Any), call it with
        # the supplied arguments and bind the returned coroutine
        # we can run it on the worker's thread-bound eventloop
        if inspect.iscoroutinefunction(task_function):
            task_function = task_function(*args, **kwargs)

        # If the supplied function is actually a vanilla Python
        # function (i.e. def any_function() -> Any), use asyncio's  # noqa
        # `to_thread` utility to wrap it along the supplied arguments
        # and bind the returned coroutine we can run it on the
        # worker's thread-bound eventloop
        if callable(task_function) and not bool(
            inspect.iscoroutine(task_function) or aio.isfuture(task_function)
        ):
            task_function = aio.to_thread(
                task_function,
                *args,
                **kwargs,
            )

        # If the value of `task_function` isn't actually something
        # that can be awaited (i.e. run on an async eventloop),
        # return it as it's either the actual result of having
        # called and run `task_function` -or- it's something we
        # can't meaningfully do anything with anyway
        if not inspect.isawaitable(task_function):
            return task_function

        # At this point, we're guaranteed to have something
        # that's either an actual coroutine or some other kind
        # of `asyncio.Future` which means we need to throw it
        # onto the worker's thread-bound eventloop to be run
        result: aio.Future = aio.run_coroutine_threadsafe(
            task_function,
            self.loop,
        )

        # Once the future has been awaited, it will either
        # have raised an exception or returned a result. If it
        # raised an exception, propagate it back to the caller
        if error := result.exception():
            raise error

        # If no exception was raised, pass `.result()` back through
        # `AsyncIOPool.run` so that it can be checked to ensure it's
        # properly handled in case another callable or awaitable was
        # returned
        return self.run(result.result())

    @classmethod
    def run_in_pool(
        cls,
        task_function: AnyCallable | AnyCoroutine,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run the supplied task in the pool's thread-bound async loop."""
        if not (worker_pool := cls.singleton):
            worker_pool = cls()

        return worker_pool.run(
            task_function,
            *args,
            **kwargs,
        )

    async def shutdown(self) -> None:
        """Shut down the worker pool."""
        if self.loop.is_running():
            self.loop.stop()
            await self.loop.shutdown_asyncgens()

        if not self.loop.is_closed() and callable(
            (
                closer := getattr(
                    self.loop,
                    "aclose",   # noqa
                    None,
                )
            )
        ):
            await closer()

    def join(self) -> None:
        """Join the loop-runner thread."""
        self.loop_runner.join()

    def on_apply(
        self,
        target: AnyCallable | AnyCoroutine,
        args: tuple[Any, ...] = tuple(),
        kwargs: Optional[dict[str, Any]] = None,
        callback: Optional[AnyCallable | AnyCoroutine] = None,
        accept_callback: [AnyCallable | AnyCoroutine] = None,
        pid: Optional[int] = None,
        getpid: Callable[[], int] = os.getpid,  # noqa
        propagate: tuple[AnyException, ...] = tuple(),
        monotonic: Callable[[], int] = time.monotonic,
        **_,
    ):
        """Apply function within pool context."""
        kwargs = kwargs or dict()
        propagate += (
            Exception,
            WorkerShutdown,
            WorkerTerminate,
        )

        if accept_callback:
            self.run(
                accept_callback,
                pid or getpid(),
                monotonic(),
            )

        try:
            ret = self.run(
                target,
                *args,
                **kwargs,
            )
        except propagate as error:
            raise error

        except BaseException as exc:
            try:
                reraise(
                    WorkerLostError,
                    WorkerLostError(repr(exc)),
                    sys.exc_info()[2],
                )
            except WorkerLostError:
                self.run(callback, ExceptionInfo())
        else:
            self.run(callback, ret)

    def terminate_job(self, pid, signal=None):
        """Terminate the specified job."""
        raise NotImplementedError

    def restart(self) -> None:
        """Restart the pool instance."""
        raise NotImplementedError
