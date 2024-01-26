import asyncio
import logging
import time
from celery import (
    Task,
    Celery
)
from celery._state import _task_stack
from typing import Any
from celery_work.configs import backend
from utils.async_pool import AsyncIOPool


logger = logging.getLogger(__name__)
WorkerPool = AsyncIOPool()


def create_celery():

    class ContextTask(Task):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.logger = logger

        def on_success(self, retval: Any, task_id: Any, args, kwargs) -> None:
            self.logger.info('Task %s succeeded: %s', task_id, retval)  # Use f-string for cleaner formatting

        def on_failure(self, exc: Exception, task_id: str, args: Any, kwargs: Any, einfo: str) -> None:
            self.logger.exception('Task failed: %s', exc, exc_info=exc)  # Include exc_info

        def run(self, *args: Any, **kwargs: Any) -> Any:
            """
            celery -A celery_work.worker worker --pool=solo -l info
            """
            start_time = time.time()
            try:
                result = super().run(*args, **kwargs)
            except Exception as exc:
                self.logger.exception('Task execution failed: %s', exc)  # Log exception within run
                raise  # Re-raise to propagate exception properly
            end_time = time.time()
            self.logger.info('Task execution time: %s seconds', end_time - start_time)
            return result

        def on_state_change(self, state: str, task_id: str, args: Any, kwargs: Any) -> None:
            self.logger.info('Task %s state changed: %s', task_id, state)

        def __call__(self, *args, **kwargs):
            _task_stack.push(self)
            self.push_request(args=args, kwargs=kwargs)
            try:
                if asyncio.iscoroutinefunction(self.run):
                    return WorkerPool.run(self.run(*args, **kwargs))
                else:
                    return self.run(*args, **kwargs)
            finally:
                self.pop_request()
                _task_stack.pop()

    _celery_: Celery = Celery("celery-job-worker", backend=backend, task_cls=ContextTask)
    _celery_.config_from_object('celery_work.configs')

    # 自动发现各个app下的tasks.py文件
    _celery_.autodiscover_tasks([
        'celery_work.tasks'
    ])

    return _celery_


celery = create_celery()
