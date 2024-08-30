import abc


class Register(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def register(self, name, id, address, port, tags, check):
        pass

    @abc.abstractmethod
    def deregister(self, service_id):
        pass

    @abc.abstractmethod
    def get_all_service(self):
        pass

    @abc.abstractmethod
    def filter_service(self, filter):
        pass
