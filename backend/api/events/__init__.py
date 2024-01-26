from typing import (
    Callable,
    TypeVar,
    Any
)

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])


class ServiceRegistryCenter:
    __handler_dict__ = {}

    def __init__(self) -> None:
        self._events = {
            "startup": [],
            "shutdown": []
        }

    @classmethod
    def register(
            cls,
            target,
            comment=None
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            if cls.contains(target):
                raise KeyError((f"\033[31m"
                                f"WARNING: {target} 已经存在!"
                                f"\033[0m"))
            cls.add_func_modules(target, func, comment)
            return func

        return decorator

    @classmethod
    def register_multi(cls, *targets):
        for target in targets:
            cls.register(target)

    @classmethod
    def register_if(cls, target, condition):
        if condition:
            cls.register(target)

    def __str__(self):
        return str(self.__handler_dict__)

    @classmethod
    def keys(cls):
        return cls.__handler_dict__.keys()

    @classmethod
    def values(cls):
        return cls.__handler_dict__.values()

    @classmethod
    def items(cls):
        return cls.__handler_dict__.items()

    @classmethod
    def get(cls, target, *args, **kwargs):
        return cls.__handler_dict__.get(target)(*args, **kwargs)

    @classmethod
    def remove(cls, target):
        del cls.__handler_dict__[target]

    @classmethod
    def clear(cls):
        cls.__handler_dict__ = {}

    @classmethod
    def contains(cls, key):
        return key in cls.__handler_dict__

    @classmethod
    def iterate(cls):
        for name, value in cls.__handler_dict__.items():
            yield name, value

    @classmethod
    def register_with_meta(cls, name, value, meta=None):
        if meta is None:
            meta = {}
        cls.__handler_dict__[name] = (value, meta)

    @classmethod
    def get_with_meta(cls, name):
        value, meta = cls.__handler_dict__[name]
        return value, meta

    @classmethod
    def add_func_modules(
            cls,
            key,
            func: DecoratedCallable,
            comment=None
    ) -> None:
        cls.__handler_dict__[key] = func

    @classmethod
    def on_event(
            cls, event_type: str
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: Callable) -> Callable:
            cls.add_event_handler(event_type, func)
            return func

        return decorator

    def add_event_handler(
            self, event_type: str, func: Callable
    ) -> None:
        assert event_type in self._events  # 使用集合检查事件类型
        self._events[event_type].append(func)
