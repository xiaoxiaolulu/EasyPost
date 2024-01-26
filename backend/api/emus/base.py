from enum import Enum
from typing import (
    Optional,
    TypeVar
)


T = TypeVar("T")


class BaseEumWitchDesc(Enum):
    """
    基础的巫师描述枚举类
    """

    __slots__ = ("_name", "_desc", "_value")

    def __init__(self, name: str, desc: T, value: int = 0) -> None:
        super().__init__(name)
        self._name = name
        self._desc = desc
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def desc(self) -> T:
        return self._desc

    @property
    def value(self) -> int:
        return self._value

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_value(cls, value: int) -> "BaseEumWitchDesc":
        """
        根据值获取枚举常量

        :param value: 值
        :return: 枚举常量
        """
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"找不到值为 {value} 的枚举常量")

    @property
    def extra_info(self) -> Optional[T]:
        """
        获取额外信息

        :return: 额外信息
        """
        return f"额外信息：{self._name} 的额外信息"
