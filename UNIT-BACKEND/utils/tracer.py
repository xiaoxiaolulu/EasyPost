"""A custom implementation of Celery's built-in `build_tracer`
utility."""

# pylint: unused-argument

# Future Imports
from __future__ import annotations

# Standard Library Imports
import logging
import os
import time
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

# Third-Party Imports
import celery
import celery.app
import celery.app.task
import celery.app.trace
import celery.canvas
import celery.exceptions
import celery.loaders
import celery.loaders.app
from celery.app.trace import (
    AsyncResult,
    BackendGetMetaError,
    Context,
    EncodeError,
    ExceptionInfo,
    FAILURE,
    gethostname,
    get_task_name,
    group,
    Ignore,
    IGNORED,
    IGNORE_STATES,
    info,
    InvalidTaskError,
    logger,
    LOG_IGNORED,
    LOG_SUCCESS,
    Reject,
    REJECTED,
    report_internal_error,
    Retry,
    RETRY,
    safe_repr,
    saferepr,
    send_postrun,
    send_prerun,
    send_success,
    _signal_internal_error,
    signals,
    STARTED,
    SUCCESS,
    successful_requests,
    task_has_custom,
    _task_stack,
    traceback_clear,
    TraceInfo,
    trace_ok_t
)

# Package-Level Imports
from utils.async_pool import AnyException


__all__ = ("build_async_tracer",)


# noinspection PyUnusedLocal
def build_async_tracer(
        name: str,
        task: Union[celery.Task, celery.local.PromiseProxy],
        loader: Optional[celery.loaders.app.AppLoader] = None,
        hostname: Optional[str] = None,
        store_errors: bool = True,
        Info: Type[TraceInfo] = TraceInfo,
        eager: bool = False,
        propagate: bool = False,
        app: Optional[celery.Celery] = None,
        monotonic: Callable[[], int] = time.monotonic,
        trace_ok_t: Type[trace_ok_t] = trace_ok_t,
        IGNORE_STATES: FrozenSet[str] = IGNORE_STATES) -> \
        Callable[[str, tuple[Any, ...], dict[str, Any], Any], trace_ok_t]:
    """Return a function that traces task execution.

    Catches all exceptions and updates result UNIT-BACKEND with the
    state and result.

    If the call was successful, it saves the result to the task result
    UNIT-BACKEND, and sets the task status to `"SUCCESS"`.

    If the call raises :exc:`~@Retry`, it extracts
    the original exception, uses that as the result and sets the task state
    to `"RETRY"`.

    If the call results in an exception, it saves the exception as the task
    result, and sets the task state to `"FAILURE"`.

    Return a function that takes the following arguments:

        uuid: The id of the task.
        args: List of positional args to pass on to the function.
        kwargs: Keyword arguments mapping to pass on to the function.
        request: Request dict.
    """

    # pylint: disable=too-many-statements

    # If the task doesn't define a custom __call__ method
    # we optimize it away by simply calling the run method directly,
    # saving the extra method call and a line less in the stack trace.
    fun = task if task_has_custom(task, '__call__') else task.run

    loader = loader or app.loader
    ignore_result = task.ignore_result
    track_started = task.track_started
    track_started = not eager and (task.track_started and not ignore_result)

    # #6476
    if eager and not ignore_result and task.store_eager_result:
        publish_result = True
    else:
        publish_result = not eager and not ignore_result

    deduplicate_successful_tasks = ((app.conf.task_acks_late or task.acks_late)
                                    and app.conf.worker_deduplicate_successful_tasks
                                    and app.backend.persistent)

    hostname = hostname or gethostname()
    inherit_parent_priority = app.conf.task_inherit_parent_priority

    loader_task_init = loader.on_task_init
    loader_cleanup = loader.on_process_cleanup

    task_before_start = None
    task_on_success = None
    task_after_return = None
    if task_has_custom(task, 'before_start'):
        task_before_start = task.before_start
    if task_has_custom(task, 'on_success'):
        task_on_success = task.on_success
    if task_has_custom(task, 'after_return'):
        task_after_return = task.after_return

    pid = os.getpid()

    request_stack = task.request_stack
    push_request = request_stack.push
    pop_request = request_stack.pop
    push_task = _task_stack.push
    pop_task = _task_stack.pop
    _does_info = logger.isEnabledFor(logging.INFO)
    resultrepr_maxsize = task.resultrepr_maxsize

    prerun_receivers = signals.task_prerun.receivers
    postrun_receivers = signals.task_postrun.receivers
    success_receivers = signals.task_success.receivers

    # Third-Party Imports
    from celery import canvas

    # Package-Level Imports
    from utils.async_pool import AsyncIOPool

    signature = canvas.maybe_signature  # maybe_ does not clone if already

    # noinspection PyUnusedLocal
    def on_error(
            request: celery.app.task.Context,
            exc: AnyException,
            state: str = FAILURE,
            call_errbacks: bool = True) -> Tuple[Info, Any, Any, Any]:
        """Handle any errors raised by a `Task`'s execution."""
        if propagate:
            raise
        I = Info(state, exc)
        R = I.handle_error_state(
            task, request, eager=eager, call_errbacks=call_errbacks,
        )
        return I, R, I.state, I.retval

    def trace_task(
            uuid: str,
            args: Sequence[Any],
            kwargs: Dict[str, Any],
            request: Optional[Dict[str, Any]] = None) -> trace_ok_t:
        """Execute and trace a `Task`."""

        # R      - is the possibly prepared return value.
        # I      - is the Info object.
        # T      - runtime
        # Rstr   - textual representation of return value
        # retval - is the always unmodified return value.
        # state  - is the resulting task state.

        # This function is very long because we've unrolled all the calls
        # for performance reasons, and because the function is so long
        # we want the main variables (I, and R) to stand out visually from the
        # the rest of the variables, so breaking PEP8 is worth it ;)
        R = I = T = Rstr = retval = state = None
        task_request = None
        time_start = monotonic()
        try:
            try:
                callable(kwargs.items)
            except AttributeError:
                raise InvalidTaskError(
                    'Task keyword arguments is not a mapping')

            task_request = Context(request or {}, args=args,
                                   called_directly=False, kwargs=kwargs)

            # TODO(the-wondersmith): Investigate if there are any potential
            #                        side effects of performing this update
            task.request.update(task_request.__dict__)

            redelivered = (task_request.delivery_info
                           and task_request.delivery_info.get('redelivered', False))
            if deduplicate_successful_tasks and redelivered:
                if task_request.id in successful_requests:
                    return trace_ok_t(R, I, T, Rstr)
                r = AsyncResult(task_request.id, app=app)

                try:
                    state = r.state
                except BackendGetMetaError:
                    pass
                else:
                    if state == SUCCESS:
                        info(LOG_IGNORED, {
                            'id': task_request.id,
                            'name': get_task_name(task_request, name),
                            'description': 'Task already completed successfully.'
                        })
                        return trace_ok_t(R, I, T, Rstr)

            push_task(task)
            root_id = task_request.root_id or uuid
            task_priority = task_request.delivery_info.get('priority') if \
                inherit_parent_priority else None
            push_request(task_request)
            try:
                # -*- PRE -*-
                if prerun_receivers:
                    send_prerun(sender=task, task_id=uuid, task=task,
                                args=args, kwargs=kwargs)
                AsyncIOPool.run_in_pool(loader_task_init, uuid, task)
                if track_started:
                    task.backend.store_result(
                        uuid, {'pid': pid, 'hostname': hostname}, STARTED,
                        request=task_request,
                    )

                # -*- TRACE -*-
                try:
                    if task_before_start:
                        AsyncIOPool.run_in_pool(task_before_start, uuid, args,
                                                kwargs)

                    R = retval = AsyncIOPool.run_in_pool(fun, *args, **kwargs)
                    state = SUCCESS
                except Reject as exc:
                    I, R = Info(REJECTED, exc), ExceptionInfo(internal=True)
                    state, retval = I.state, I.retval
                    I.handle_reject(task, task_request)
                    traceback_clear(exc)
                except Ignore as exc:
                    I, R = Info(IGNORED, exc), ExceptionInfo(internal=True)
                    state, retval = I.state, I.retval
                    I.handle_ignore(task, task_request)
                    traceback_clear(exc)
                except Retry as exc:
                    I, R, state, retval = on_error(
                        task_request, exc, RETRY, call_errbacks=False)
                    traceback_clear(exc)
                except Exception as exc:
                    I, R, state, retval = on_error(task_request, exc)
                    traceback_clear(exc)
                except BaseException:
                    raise
                else:
                    try:
                        # callback tasks must be applied before the result is
                        # stored, so that result.children is populated.

                        # groups are called inline and will store trail
                        # separately, so need to call them separately
                        # so that the trail's not added multiple times :(
                        # (Issue #1936)
                        callbacks = task.request.callbacks
                        if callbacks:
                            if len(task.request.callbacks) > 1:
                                sigs, groups = [], []
                                for sig in callbacks:
                                    sig = signature(sig, app=app)
                                    if isinstance(sig, group):
                                        groups.append(sig)
                                    else:
                                        sigs.append(sig)
                                for group_ in groups:
                                    group_.apply_async(
                                        (retval,),
                                        parent_id=uuid, root_id=root_id,
                                        priority=task_priority
                                    )
                                if sigs:
                                    group(sigs, app=app).apply_async(
                                        (retval,),
                                        parent_id=uuid, root_id=root_id,
                                        priority=task_priority
                                    )
                            else:
                                signature(callbacks[0], app=app).apply_async(
                                    (retval,), parent_id=uuid, root_id=root_id,
                                    priority=task_priority
                                )

                        # execute first task in chain
                        chain = task_request.chain
                        if chain:
                            _chsig = signature(chain.pop(), app=app)
                            _chsig.apply_async(
                                (retval,), chain=chain,
                                parent_id=uuid, root_id=root_id,
                                priority=task_priority
                            )
                        task.backend.mark_as_done(
                            uuid, retval, task_request, publish_result,
                        )
                    except EncodeError as exc:
                        I, R, state, retval = on_error(task_request, exc)
                    else:
                        Rstr = saferepr(R, resultrepr_maxsize)
                        T = monotonic() - time_start
                        if task_on_success:
                            AsyncIOPool.run_in_pool(task_on_success, retval,
                                                    uuid, args, kwargs)
                        if success_receivers:
                            send_success(sender=task, result=retval)
                        if _does_info:
                            info(LOG_SUCCESS, {
                                'id': uuid,
                                'name': get_task_name(task_request, name),
                                'return_value': Rstr,
                                'runtime': T,
                                'args': safe_repr(args),
                                'kwargs': safe_repr(kwargs),
                            })

                # -* POST *-
                if state not in IGNORE_STATES:
                    if task_after_return:
                        AsyncIOPool.run_in_pool(task_after_return,
                            state, retval, uuid, args, kwargs, None,
                        )
            finally:
                try:
                    if postrun_receivers:
                        send_postrun(sender=task, task_id=uuid, task=task,
                                     args=args, kwargs=kwargs,
                                     retval=retval, state=state)
                finally:
                    pop_task()
                    pop_request()
                    if not eager:
                        try:
                            task.backend.process_cleanup()
                            AsyncIOPool.run_in_pool(loader_cleanup)
                        except (KeyboardInterrupt, SystemExit, MemoryError):
                            raise
                        except Exception as exc:
                            logger.error('Process cleanup failed: %r', exc,
                                         exc_info=True)
        except MemoryError:
            raise
        except Exception as exc:
            _signal_internal_error(task, uuid, args, kwargs, request, exc)
            if eager:
                raise
            R = report_internal_error(task, exc)
            if task_request is not None:
                I, _, _, _ = AsyncIOPool.run_in_pool(on_error, task_request,
                                                     exc)
        return trace_ok_t(R, I, T, Rstr)

    return trace_task
