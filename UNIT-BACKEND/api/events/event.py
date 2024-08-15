from abc import ABC


class Cancelable(ABC):
    _is_canceled: bool

    def __init__(self, is_canceled: bool = False):
        self._is_canceled = is_canceled

    def is_canceled(self):
        """
        :return: 该事件是否被取消
        """
        return self._is_canceled

    def cancel(self):
        """
        取消该事件
        """
        self._is_canceled = True


class Event(ABC):
    ...
