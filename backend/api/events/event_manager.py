import asyncio
from typing import (
    List,
    Dict,
    Callable,
    Coroutine,
    Any,
    TypeVar,
    Optional
)
from typing import Type as Class
from inspect import (
    signature,
    Signature,
    Parameter
)
from api.events.event import (
    Event,
    Cancelable
)
from api.exception.events import (
    UnsupportedFunctionException,
    IllegalEventException
)


E = TypeVar('E', bound=Event)
EventHandler = Callable[[E], Coroutine[Any, Any, Any]]


class EventManager:

    map: Dict[Class[Event], List[EventHandler]] = {}

    @classmethod
    async def post(
            cls,
            context: Event | Cancelable = None,
            alias: Optional[str] = None,
            callback: Callable[[], Coroutine[Any, Any, Any]] = None):
        """
        发布事件
        :usage:
            event = MyEvent("Hello, world!")
            EventManager.post(event, "vent")
        :param context: 事件内容
        :param alias: 事件别名
        :param callback: 事件回调（仅在事件可取消且未被取消时进行）
        :return:
        """
        key = alias or context.__class__
        func_list: List[EventHandler] = cls.map.get(key, [])
        for i in func_list:
            await i(context)
        if issubclass(context.__class__, Cancelable) and not context.is_canceled():
            await callback()

    @classmethod
    def unsubscribe_all(cls):
        """取消所有事件的所有订阅"""
        cls.map.clear()

    @classmethod
    def unsubscribe_by_alias(
            cls,
            context: Event | Cancelable = None,
            alias: Optional[str] = None,
    ):
        """取消对指定事件别名的所有订阅"""
        key = alias or context.__class__
        del cls.map[key]

    @classmethod
    def subscribe(cls, alias: Optional[str] = None):
        """
        订阅事件
        :param alias: 事件别名
        :usage:
            @EventManager.subscribe("Event")
        """

        def decorator(handler: EventHandler):
            sign: Signature = signature(handler)
            params: List[Parameter] = list(sign.parameters.values())
            if len(params) != 1:
                raise UnsupportedFunctionException('Params lens not match.')
            event_type: Class[Event] = params[0].annotation

            event_key = alias or event_type
            func_list: List[EventHandler] = cls.map.get(event_key, [])
            if not issubclass(event_type, Event):
                raise IllegalEventException()
            if not asyncio.iscoroutinefunction(handler):
                raise UnsupportedFunctionException('Is not coroutine function.')
            else:
                func_list.append(handler)
                cls.map[event_key] = func_list

        return decorator
