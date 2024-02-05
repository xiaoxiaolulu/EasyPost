from abc import abstractmethod


class BaseScheduler(metaclass=type):

    @abstractmethod
    def configure(self, **kwargs) -> int:
        ...

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def remove(self, plan_id: int):
        ...
