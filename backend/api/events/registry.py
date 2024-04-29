from typing import (
    Dict,
    Optional,
    Iterator
)


class Registry:

    def __init__(self, name: str) -> None:
        """
        Initializes a registry with a given name.

        Args:
            name (str): The name of the registry.
        """
        self._name: str = name
        self._obj_map: Dict[str, object] = {}

    def _register(self, name: str, obj: object, *, suffix: str = None) -> None:
        """
        Registers an object in the registry.

        Args:
            name (str): The name of the object to register.
            obj (object): The object to register.
            suffix (str, optional): An optional suffix to append to the name
                if there's a naming conflict. Defaults to None.

        Raises:
            AssertionError: If an object with the same name (or name with suffix)
                is already registered.
        """
        if suffix:
            name = f"{name}_{suffix}"  # F-string for cleaner string formatting
        assert name not in self._obj_map, f"Object '{name}' already registered in '{self._name}'!"
        self._obj_map[name] = obj
        print(name)
        print(self._obj_map)

    def register(self, name: str = None, obj: Optional[object] = None, *, suffix: str = None) -> Optional[callable]:
        """
        Registers an object in the registry.

        This method can be used as a decorator or as a function call.

        Args:
            name (str): The name of the object to register.
            obj (object, optional): The object to register. Defaults to None.
            suffix (str, optional): An optional suffix to append to the name
                if there's a naming conflict. Defaults to None.

        Returns:
            callable: The decorator if used as such, otherwise None.
        """
        if obj is None:
            def decorator(func_or_class: callable) -> callable:

                registry_name = func_or_class.__name__ if name is None else name
                self._register(registry_name, func_or_class, suffix=suffix)
                return func_or_class
            return decorator

        self._register(obj.__name__, obj, suffix=suffix)

    def get(self, name: str, default_suffix: str = 'basicsr') -> object:
        """
        Retrieves an object from the registry.

        Args:
            name (str): The name of the object to retrieve.
            default_suffix (str, optional): An optional default suffix to try
                if the provided name is not found. Defaults to 'basicsr'.

        Returns:
            object: The retrieved object.

        Raises:
            KeyError: If the object with the given name (or name with default suffix)
                is not found in the registry.
        """
        obj = self._obj_map.get(name)
        if obj is None:
            obj = self._obj_map.get(f"{name}_{default_suffix}")
            if obj:
                print(f'Name {name} not found, using {name}_{default_suffix}')
        if obj is None:
            raise KeyError(f"No object named '{name}' found in '{self._name}' registry!")
        return obj

    def __contains__(self, name: str) -> bool:
        """
        Checks if the registry contains an object with the given name.

        Args:
            name (str): The name of the object to check.

        Returns:
            bool: True if the object exists in the registry, False otherwise.
        """
        return name in self._obj_map

    def __iter__(self) -> Iterator[tuple[str, object]]:
        """
        Provides an iterator for iterating over the registry entries.

        Returns:
            iterator: An iterator over key-value pairs of the registry.
        """
        return iter(self._obj_map.items())

    def keys(self) -> dict.keys:
        """
        Returns a view of all object names registered in the registry.

        Returns:
            view: A view object containing the names of the registered objects.
        """
        return self._obj_map.keys()


registry = Registry('service_registry')
