import time

from requests import Response
import importlib
import json
import os
import re
import unittest
from functools import wraps
from numbers import Number
from typing import (
    Callable,
    Any
)
from unittest import TestSuite
import requests
from jsonpath import jsonpath
from requests_toolbelt import MultipartEncoder
from core.request.runner import TestRunner
from utils.DBClient import DBClient


try:
    global_func = importlib.import_module('global_func')
except ModuleNotFoundError:
    from utils import builtin as global_func


class BaseEnv(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __getattr__(self, item):
        return super().__getitem__(item)


ENV = BaseEnv()
db = DBClient()
DEBUG = True
session = requests.Session()


class GenerateCase:
    """解析数据创建测试用例"""

    def __init__(self):
        self.controller = BaseTest()

    def data_to_suite(self, datas) -> TestSuite:
        """
        根据用例数据生成测试套件
        :param datas:
        :return:
        """
        suite = unittest.TestSuite()
        load = unittest.TestLoader()
        for item in datas:
            cls = self.create_test_class(item)
            suite.addTest(load.loadTestsFromTestCase(cls)) # noqa
        return suite

    def create_test_class(self, item) -> type:
        """创建测试类"""
        cls_name = item.get('name') or 'Demo'
        cases = item.get('cases')
        # 创建测试类
        cls = type(cls_name, (BaseTest,), {})
        # 遍历数据生成,动态添加测试方法
        for index, case_ in enumerate(cases):
            if_request_obj = case_.get('IF', None)
            test_name = self.create_test_name(index, len(cases))
            new_test_func = self.create_test_func(getattr(cls, 'step'), case_)
            new_test_func.__doc__ = case_.get('title') or new_test_func.__doc__
            setattr(cls, test_name, new_test_func)

            if if_request_obj:
                test_item = getattr(cls, test_name)
                condition = if_request_obj.get('condition', True)
                reason = if_request_obj.get('reason', '跳过')
                self.controller.skipIf(condition, reason, test_item)

        return cls

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


class CaseRunLog:

    def save_log(self, message, level) -> None:
        if not hasattr(self, 'log_data'):
            setattr(self, 'log_data', [])
        info = "【{}】 |: {}".format(level, message)
        getattr(self, 'log_data').append(info)
        print(info)

    def save_validators(self, methods, expected, actual, result) -> None:
        if not hasattr(self, 'validate_extractor'):
            setattr(self, 'validate_extractor', [])
        info = "预期结果: {} {} 实际结果: {} {}".format(expected, methods, actual, result)
        getattr(self, 'validate_extractor').append(info)

    def save_ife(self, info) -> None:
        if not hasattr(self, 'if_extractor'):
            setattr(self, 'if_extractor', [])
        getattr(self, 'if_extractor').append(info)

    def print(self, *args) -> None:
        args = [str(i) for i in args]
        message = ' '.join(args)
        getattr(self, 'log_data').append(('INFO', message))

    def debug_log(self, *args) -> None:
        if DEBUG:
            message = ''.join(args)
            self.save_log(message, 'DEBUG')

    def info_log(self, *args) -> None:
        message = ''.join(args)
        self.save_log(message, 'INFO')

    def warning_log(self, *args) -> None:
        message = ''.join(args)
        self.save_log(message, 'WARNING')

    def error_log(self, *args) -> None:
        message = ''.join(args)
        self.save_log(message, 'ERROR')

    def exception_log(self, *args) -> None:
        message = ''.join(args)
        self.save_log(message, 'ERROR')

    def critical_log(self, *args) -> None:
        message = ''.join(args)
        self.save_log(message, 'CRITICAL')


class BaseTest(unittest.TestCase, CaseRunLog):

    def timer(self, second) -> None:
        """
        等待控制器
        """
        time.sleep(second)
        self.info_log('强制等待:{}秒'.format(second))

    @staticmethod
    def skipIf(condition, reason, item):
        """
        条件控制器
        """
        if condition:
            item.__unittest_skip__ = True
            item.__unittest_skip_why__ = reason
        return item

    @classmethod
    def setUpClass(cls) -> None:
        cls.env = BaseEnv()
        if DEBUG:
            cls.session = session
        else:
            cls.session = requests.Session()

    def step(self, data) -> None:
        """执行单条用例的主函数"""
        # 强制等待
        sleep = data.get('timer', 0)
        self.timer(sleep)
        # 日志记录
        self.__run_log()
        # 执行前置脚本
        self.__run_setup_script(data)
        # 发送请求
        response = self.__send_request(data)
        # 断言
        checks = data.get('validators')
        self.validators(response.json(), checks)
        # print("ifelsexxx")
        # if_e = data.get('if', None)
        # print(if_e)
        # self.validators(4, if_e, method=True)
        # print("跳过了")
        # 执行后置脚本
        self.__run_teardown_script(response)

    def validators(self, response: Any, validate_check) -> None:

        if isinstance(validate_check, list):
            for check in validate_check:
                methods = check.get('method', None)
                expect = check.get('expect', None)
                expect_result = self.json_extract(response, expect)
                actual = check.get('actual', None)
                self.assertion(methods, expect_result, actual)

    def __run_log(self) -> None:
        """输出当前环境变量数据的日志"""
        self.l_env = ['\t{}:{}\n'.format(k, repr(v)) for k, v in self.env.items()]
        self.g_env = ['\t{}:{}\n'.format(k, repr(v)) for k, v in ENV.items()]
        self.info_log('当前运行环境\n',
                      "临时变量：\n{}".format(''.join(self.l_env)),
                      "全局变量：\n{}".format(''.join(self.g_env)))

    def __request_log(self) -> None:
        """请求信息日志输出"""
        self.debug_log("请求头：\n{}".format(self.requests_header))
        self.debug_log("请求体：\n{}".format(self.requests_body))
        self.debug_log("响应头：\n{}".format(self.response_header))
        self.debug_log("响应体：\n{}".format(self.response_body))
        self.info_log('请求响应状态码:{}'.format(self.status_cede))

    def __send_request(self, data) -> Response:
        """发送请求"""
        request_info = self.__handler_request_data(data)
        self.info_log('发送请求[{}]:{}：'.format(request_info['method'].upper(), request_info['url']))
        try:
            response = session.request(**request_info)
        except Exception as e:
            raise ValueError('请求发送失败，错误信息如下：{}'.format(e))
        self.url = response.request.url
        self.method = response.request.method
        self.status_cede = response.status_code

        self.response_header = json.dumps(dict(response.headers), ensure_ascii=False, indent=2)
        self.requests_header = json.dumps(dict(response.request.headers), ensure_ascii=False, indent=2)
        try:
            response_body = response.json()
            self.response_body = json.dumps(response_body, ensure_ascii=False, indent=2)
        except (Exception,):
            body = response.content
            self.response_body = body.decode('utf-8') if body else ''
        try:
            request_body = json.loads(response.request.body.decode('utf-8'))
            self.requests_body = json.dumps(request_body, ensure_ascii=False, indent=2)
        except (Exception,):
            body = response.request.body
            self.requests_body = body or ''
        self.__request_log()
        return response

    def __handler_request_data(self, data) -> dict[str | Any, Any]:
        """处理请求数据"""
        # 获取请求头
        if ENV.get('headers'):
            data['headers'] = ENV.get('headers').update(data.get('headers'))
        # 替换用例数据中的变量
        for k, v in list(data.items()):
            if k not in ['setup_script', "run_teardown_script"]:
                # 替换变量
                v = self.__parser_variable(v)
                data[k] = v
        # files字段文件上传处理的处理
        files = data.get('files')
        if files:
            if isinstance(files, dict):
                file_data = files.items()
            else:
                file_data = files
            field = []
            for name, file_info in file_data:
                # 判断是否时文件上传(获取文件类型和文件名)
                if len(file_info) == 3 and os.path.isfile(file_info[1]):
                    field.append([name, (file_info[0], open(file_info[1], 'rb'), file_info[2])])
                else:
                    field.append([name, file_info])
            form_data = MultipartEncoder(fields=field)
            data['headers']["Content-Type"] = form_data.content_type
            data['data'] = form_data
            data['files'] = None
        else:
            if data['headers'].get("Content-Type"):
                del data['headers']["Content-Type"]
        # 组织requests 发送请求所需要的参数格式
        request_params = {}
        # requests请求所需的所有字段
        params_fields = ['url', 'method', 'params', 'data', 'json', 'files', 'headers', 'cookies', 'auth', 'timeout',
                         'allow_redirects', 'proxies', 'hooks', 'stream', 'verify', 'cert']
        for k, v in data['request'].items():
            if k in params_fields:
                request_params[k] = v
        # 请求地址
        request_params['url'] = data.get('host') or ENV.get('host') + data.get('interface').get('url')
        # 请求方法
        request_params['method'] = data.get('interface').get('method')
        # 请求头
        request_params['headers'] = data['headers']
        return request_params

    def __parser_variable(self, data) -> str | None | Any:
        """替换变量"""
        pattern = r'\${{(.+?)}}'
        old_data = data
        """解析变量"""
        if isinstance(data, str):
            while re.search(pattern, data):
                res2 = re.search(pattern, data)
                item = res2.group()
                attr = res2.group(1)
                value = ENV.get(attr) if self.env.get(attr) is None else self.env.get(attr)
                if value is None:
                    raise ValueError('变量引用错误:\n{}中的变量{},在当前运行环境中未找到'.format(data, attr))
                if item == data:
                    return value
                data = data.replace(item, str(value))
            return data
        elif isinstance(data, list) or isinstance(data, dict):
            data = str(data)
            while re.search(pattern, data):
                res2 = re.search(pattern, data)
                item = res2.group()
                attr = res2.group(1)
                value = ENV.get(attr) if self.env.get(attr) is None else self.env.get(attr)
                if value is None:
                    raise ValueError('变量引用错误：\n{}\n中的变量{},在当前运行环境中未找到'.format(
                        json.dumps(old_data, ensure_ascii=False, indent=2), attr)
                    )
                if isinstance(value, Number):
                    s = data.find(item)
                    dd = data[s - 1:s + len(item) + 1]
                    data = data.replace(dd, str(value))
                elif isinstance(value, str) and "'" in value:
                    data = data.replace(item, value.replace("'", '"'))
                else:
                    data = data.replace(item, str(value))
            return eval(data)
        else:
            return data

    def save_env_variable(self, name, value) -> None:
        self.info_log('设置临时变量\n变量名:{}\n变量值:{}'.format(name, value))
        if DEBUG:
            self.debug_log('提示调试模式运行,设置的临时变量均保存到全局变量中')
            ENV[name] = value
        else:
            self.env[name] = value

    def save_global_variable(self, name, value) -> None:
        self.info_log('设置全局变量\n变量名:{}\n变量值:{}'.format(name, value))
        ENV[name] = value

    def delete_env_variable(self, name) -> None:
        """删除临时变量"""
        self.info_log('删除临时变量:{}'.format(name, ))
        del self.env[name]

    def delete_global_variable(self, name) -> None:
        """删除全局变量"""
        self.info_log('删除全局变量:{}'.format(name))
        del ENV[name]

    def json_extract(self, obj, ext) -> Any:
        """jsonpath数据提取"""
        self.info_log('jsonpath提取数据')
        value = jsonpath(obj, ext)
        value = value[0] if value else ''
        self.info_log('\n提取表达式：{}'.format(ext), '\n提取结果:{}'.format(value))
        return value

    def re_extract(self, string, ext) -> Any:
        """正则表达式提取数据提取"""
        self.info_log('正则提取数据')
        value = re.search(ext, string)
        value = value.group(1) if value else ''
        self.info_log('\n提取表达式：{}'.format(ext), '\n提取结果:{}'.format(value))
        return value

    def assertion(self, methods, expected, actual) -> None:
        """
        断言
        :param methods: 比较方式
        :param expected: 预期结果
        :param actual: 实际结果
        :return:
        """
        methods_map = {
            "相等": self.assertEqual,
            "不相等": self.assertNotEqual,
            "约等于": self.assertAlmostEqual,
            "不约等于": self.assertNotAlmostEqual,
            "大于": self.assertGreater,
            "大于等于": self.assertGreaterEqual,
            "小于": self.assertLess,
            "小于等于": self.assertLessEqual,
            "包含": self.assertIn,
            "不包含": self.assertNotIn
        }
        self.info_log('断言方法:{}\n预期结果:{}\n实际结果:{}'.format(methods, expected, actual))
        assert_method = methods_map.get(methods)
        global result # noqa
        if assert_method:
            try:
                assert_method(expected, actual)
            except Exception as err:
                self.warning_log('断言失败!')
                self.save_validators(methods, expected, actual, '【❌】')
                raise self.failureException(err)
            else:
                self.info_log("断言通过!")
                self.save_validators(methods, expected, actual, '【✔】')
        else:
            raise TypeError('断言比较方法{},不支持!'.format(methods))

    def __run_script(test, data) -> None:  # noqa
        print = test.print  # noqa
        env = test.env  # noqa
        setup_script = data.get('setup_script')
        if setup_script:
            try:
                exec(setup_script)
            except Exception as e:
                test.error_log('前置脚本执行错误:\n{}'.format(e))
                delattr(test, 'hook_gen')
                raise
        response = yield  # noqa
        teardown_script = data.get('teardown_script')
        if teardown_script:
            try:
                exec(teardown_script)
            except Exception as e:
                test.error_log('后置脚本执行错误:\n{}'.format(e))
                raise
        yield

    def __run_teardown_script(self, response) -> None:
        """执行后置脚本"""
        self.info_log('执行后置脚本')
        self.hook_gen.send(response)
        delattr(self, 'hook_gen')

    def __run_setup_script(self, data):
        """执行前置脚本"""
        self.info_log('执行前置脚本')
        self.hook_gen = self.__run_script(data) # noqa
        next(self.hook_gen)  # noqa


def run_test(case_data, env_config, tester='测试员', thread_count=1, debug=True) -> tuple[Any, dict[Any, Any]] | Any:
    """
    :param case_data: 测试套件数据
    :param env_config: 用例执行的环境配置
        env_config:{
        'ENV':{"host":'http//:127.0.0.1'},
        'db':[{},{}],
        'FuncTools':'工具函数文件'
        }
    :param thread_count: 运行线程数
    :param debug: 单接口调试用debug模式
    :param tester: 测试员
    :return:
        debug模式：会返回本次运行的结果和 本次运行设置的全局变量，
    """
    global global_func, db, DEBUG, ENV  # noqa
    global_func_file = env_config.get('global_func', b'')
    if global_func:
        with open('global_func.py', 'w', encoding='utf-8') as f:
            f.write(global_func_file)
    # 更新运行环境
    global_func = importlib.reload(global_func)
    DEBUG = debug
    ENV = {**env_config.get('ENV', {})}
    db.init_connect(env_config.get('db', []))
    # 失败重跑
    rerun = env_config.get('rerun', 0)
    # 生成测试用例
    suite = GenerateCase().data_to_suite(case_data)
    # 运行测试用例
    runner = TestRunner(suite=suite, tester=tester)
    result = runner.run(thread_count=thread_count, rerun=rerun)
    if global_func:
        os.remove('global_func.py')
    # 断开数据库连接
    db.close_connect()
    if debug:
        return result, ENV
    else:
        return result
