"""
DESCRIPTION：嵌套字典解析公共方法.

:Created by Null.
"""


class GetJsonParams(object):

    @classmethod
    def get_value(cls, my_dict: dict, key: str) -> str:
        r"""解析一个嵌套字典，并获取指定key的值
        :Args:
         - my_dict: 解析的字典,  dict object.
         - key: 指定解析的键,  str object.
        :Usage:
            get_value({'hello': 'world'}, 'hello')
        """

        if isinstance(my_dict, dict):
            if my_dict.get(key) or my_dict.get(key) == 0 or my_dict.get(key) == '' \
                    and my_dict.get(key) is False or my_dict.get(key) == []:
                return my_dict.get(key)

            for my_dict_key in my_dict:
                if cls.get_value(my_dict.get(my_dict_key), key) or \
                        cls.get_value(my_dict.get(my_dict_key), key) is False:
                    return cls.get_value(my_dict.get(my_dict_key), key)

        if isinstance(my_dict, list):
            for my_dict_arr in my_dict:
                if cls.get_value(my_dict_arr, key) \
                        or cls.get_value(my_dict_arr, key) is False:
                    return cls.get_value(my_dict_arr, key)

    @classmethod
    def get_sibling_content(cls, my_dict: dict, parent_key: str, sibling_key: str, sibling_value: all,
                            same_key: str) -> str:
        r"""解析一个嵌套字典中存在相同key的情况
        :Arg:
         - my_dict: 需要解析的字典, dict object.
         - parent_key: 解析字典的父层级建，str object.
         - sibling_key: 解析字典的兄弟层级建, str object.
         - sibling_value 解析字典兄弟层级值，all object.
         - same_key: 需要取值的KEY值, str object.
        :Usage:
            get_same_content(my_dict=my_dict, list_key='datalist', list_index=0, same_key='botName')
        """
        parent_level = cls.get_value(my_dict=my_dict, key=parent_key)
        for index, content in enumerate(parent_level):
            for key, value in content.items():  # noqa
                if key == sibling_key and value == int(sibling_value):
                    return_value = cls.get_value(my_dict=my_dict, key=parent_key)[index][same_key]  # noqa
                    return return_value

    @classmethod
    def get_same_content(cls, my_dict: dict, parent_key: str, child_index: int, child_key: str):
        """
        解析字典，对于字典中存在相同键值对的情况，可以指定获取这数组中的具体第几个的键的值
        :param my_dict: 需要解析的字典: dict object.
        :param parent_key: 需要解析字典中的数组, str object.
        :param child_index: 需要解析数组中的第几个字典, int object.
        :param child_key: 需要解析数组中具体字典中的哪一个key, str object.
        :return:
        """
        child_dict = cls.get_value(my_dict=my_dict, key=parent_key)[child_index]
        return cls.get_value(dict(child_dict), child_key)  # noqa

    @classmethod
    def for_keys_to_dict(cls, *args: tuple, my_dict: dict, value_type: bool = False) -> dict:
        r"""指定多个key，并获取一个字典的多个对应的key，组成一个新的字典

        :Arg:
         - args: 指定的key值, tuple object.
         - my_dict: 解析的字典, dict object.
         - value_type: 是否将参数类型转化为str object, 默认为False, bool object;
        :Usage:
            for_keys_to_do_dict('hello', {'hello': 'hello'})
        """
        result = {}
        if len(args) > 0:
            for key in args:
                value = cls.get_value(my_dict, str(key))
                value = str(value) if value_type else value
                result.update({key: value})
        return result
