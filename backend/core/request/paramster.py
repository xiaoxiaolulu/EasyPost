from functools import wraps
import json
import yaml


def _create_test_name(index, name):
    if index + 1 < 10:
        test_name = name + "_00" + str(index + 1)
    elif index + 1 < 100:
        test_name = name + "_0" + str(index + 1)
    else:
        test_name = name + "_" + str(index + 1)
    return test_name


def _update_func(new_func_name, params, test_desc, func, *args, **kwargs):
    @wraps(func)
    def wrapper(self):
        return func(self, params, *args, **kwargs)

    wrapper.__wrapped__ = func
    wrapper.__name__ = new_func_name
    wrapper.__doc__ = test_desc
    return wrapper


def ddt(cls):
    """
    :param cls: 测试类
    :return:
    """
    for name, func in list(cls.__dict__.items()):
        if hasattr(func, "PARAMS"):

            for index, case_data in enumerate(getattr(func, "PARAMS")):
                print(index)
                print(case_data)
                new_test_name = _create_test_name(index, name)
                if isinstance(case_data, dict) and case_data.get("title"):
                    test_desc = str(case_data.get("title"))
                elif isinstance(case_data, dict) and case_data.get("desc"):
                    test_desc = str(case_data.get("desc"))
                elif (not isinstance(case_data, str)) and hasattr(case_data, 'title'):
                    test_desc = str(case_data.title)
                else:
                    test_desc = func.__doc__

                func2 = _update_func(new_test_name, case_data, test_desc, func)
                setattr(cls, new_test_name, func2)
            else:
                delattr(cls, name)
    return cls


def list_data(datas):
    """
    :param datas: 测试数据
    :return:
    """

    def wrapper(func):
        setattr(func, "PARAMS", datas)
        return func

    return wrapper
