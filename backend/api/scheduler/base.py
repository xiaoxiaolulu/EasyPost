from abc import abstractmethod


class BaseScheduler(metaclass=type):

    @abstractmethod
    def configure(self, **kwargs) -> int:
        """
        This method is an abstract method that must be implemented by child classes.
        It is used to configure the instance with the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to pass to the configuration process.

        Returns:
            int: The return value of the configuration process. The specific meaning of this value
                is up to the implementation of the child class.
        """
        ...

    @abstractmethod
    def start(self):
        """
        This method is an abstract method that must be implemented by child classes.
        It is used to start the instance.

        Args:
            None: This method does not take any arguments.

        Returns:
            None: The method does not return any value.
        """
        ...

    @abstractmethod
    def remove(self, plan_id: int):
        """
        This method is an abstract method that must be implemented by child classes.
        It is used to remove a test plan with the given ID.

        Args:
            plan_id: The unique identifier of the test plan to be removed.

        Returns:
            None: The method does not return any value.
        """
        ...
