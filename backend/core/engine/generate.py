import unittest
from functools import wraps
from typing import (
    Callable,
    Any
)
from unittest import TestSuite
from core.engine.base import BaseTest
from core.models import step


class GenerateCase:
    """解析数据创建测试用例"""

    def __init__(self):
        self.controller = BaseTest()

    def data_to_suite(self, datas: step.TestCase) -> TestSuite:
        """
        根据用例数据生成测试套件
        :param datas:
        :return:
        """
        suite = unittest.TestSuite()
        load = unittest.TestLoader()
        if isinstance(datas, list):
            for item in datas:
                self.add_test(item, load, suite)
            return suite

        if isinstance(datas, dict):
            self.add_test(datas, load, suite)
            return suite

    def add_test(self, item, load, suite):
        cls = self.create_test_class(item)
        suite.addTest(load.loadTestsFromTestCase(cls))  # noqa

    def create_test_class(self, item) -> type:
        """创建测试类"""
        cls_name = item.get('name') or 'Demo'

        cases = item.get('cases', None)

        collections = cases if cases is not None else [item]

        # 创建测试类
        cls = type(cls_name, (BaseTest,), {})
        # 遍历数据生成,动态添加测试方法
        self.create_case_content(cls, collections)

        return cls

    def create_case_content(self, cls, cases, skip_collections: list = [], loop_collections: list = []):
        """
        生成用例内容模版, 目前支持嵌套循环控制器与if控制器(不超过2层)
        {
         Loop: 3,
         children: [
            Loop: 2,
            ....
         ]
        }
        """
        for index, case_ in enumerate(cases):
            mode = case_.get('mode', 'normal')
            if mode == 'normal':
                global children # noqa
                try:
                    children = case_.get('children', None)
                except AttributeError:
                    pass

                if children:
                    skip_after = case_.get('If', {'condition': False})
                    loop_after = case_.get('Loop', 1)
                    skip_collections.append(skip_after)
                    loop_collections.append(loop_after)

                    self.create_case_content(cls, children, skip_collections, loop_collections)
                else:
                    if_before = case_.get('If', {'condition': False})
                    loop_before = case_.get('Loop', 1)
                    skip_collections.append(if_before)
                    loop_collections.append(loop_before)

                    # 计算当前执行用例循环次数
                    loop_count = self.controller.loop_strategy(loop_collections)
                    # 计算当前执行用例是否跳过
                    if_object = self.controller.skip_strategy(skip_collections)

                    test_name = self.create_test_name(index, len(cases))
                    new_test_func = self.create_test_func(getattr(cls, 'step'), case_)
                    new_test_func.__doc__ = case_.get('title') or new_test_func.__doc__

                    # 循环当前用例, 默认1次
                    self.controller.loop(loop_count, cls, test_name, new_test_func)

                    test_name = [name for name in cls.__dict__.keys() if name.__contains__('test_')]

                    self.controller.skipIf(if_object, cls, str(test_name.pop()))

            else:

                test_name = self.create_test_name(index, len(cases))
                new_test_func = self.create_test_func(getattr(cls, 'perform'), case_)
                new_test_func.__doc__ = case_.get('title') or new_test_func.__doc__
                setattr(cls, test_name, new_test_func)

    def create_test_func(self, func, case_) -> Callable[[Any], None]:
        """创建测试方法"""

        @wraps(func)
        def wrapper(self):  # noqa
            func(self, case_)

        return wrapper

    @staticmethod
    def create_test_name(index, length) -> str:
        """生成测试方法名"""
        n = (len(str(length)) // len(str(index))) - 1
        test_name = 'test_{}'.format("0" * n + str(index + 1))
        return test_name
