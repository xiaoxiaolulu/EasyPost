import time
import numpy as np
from pymeter.api.config import (
    TestPlan,
    ThreadGroupSimple
)
from pymeter.api.samplers import HttpSampler
from requests import Response
import json
import os
import re
import unittest
from numbers import Number
from typing import Any
import requests
from jsonpath import jsonpath
from requests_toolbelt import MultipartEncoder
from core.engine.env import (
    BaseEnv,
    DEBUG,
    session,
    ENV
)
from core.engine.log import CaseRunLog


class BaseTest(unittest.TestCase, CaseRunLog):

    """用例执行逻辑"""

    def timer(self, second) -> None:
        """
        等待控制器
        """
        time.sleep(second)
        self.info_log('⏯️强制等待:{}秒\n'.format(second))

    @staticmethod
    def skipIf(_condition, cls, test_name):
        """
        条件控制器
        """
        test_item = getattr(cls, test_name)

        try:
            if _condition:
                test_item.__unittest_skip__ = True
                test_item.__unittest_skip_why__ = 'Skip'
            return test_item

        except (AttributeError, ):
            return test_item

    def loop(self, loop_obj, cls, test_name, new_test_func):
        """循环控制器"""

        count = 1 if loop_obj is None else loop_obj # noqa
        for c in range(int(count)):
            tag = f'_NoLooP_' if loop_obj is None else f'_Loop_{c + 1}'
            setattr(cls, f"{test_name + tag}", new_test_func)
            self.info_log('🔁用例第{}次循环\n'.format(c + 1))

    def save_env_variable(self, name, value) -> None:
        """
        设置一个环境变量
        """
        self.info_log('♾️设置临时变量 变量名:{} 变量值:{}\n'.format(name, value))
        if DEBUG:
            self.debug_log('⏭️提示调试模式运行,设置的临时变量均保存到全局变量中\n')
            ENV[name] = value
        else:
            self.env[name] = value

    def get_env_variable(self, name) -> str:
        """
        获取一个环境变量
        """
        self.info_log('♾️获取临时变量 变量名:{}\n'.format(name))
        if DEBUG:
            return ENV[name]
        else:
            return self.env[name]

    def get_pre_url(self) -> str:
        """获取当前环境的url"""
        pre_url = self.get_env_variable('url')
        return pre_url

    def save_global_variable(self, name, value) -> None:
        """设置全局环境变量"""
        self.info_log('♾️设置全局变量 变量名:{} 变量值:{}\n'.format(name, value))
        ENV[name] = value

    def delete_env_variable(self, name) -> None:
        """删除临时变量"""
        self.info_log('♾️删除临时变量:{}\n'.format(name, ))
        del self.env[name]

    def delete_global_variable(self, name) -> None:
        """删除全局变量"""
        self.info_log('♾️删除全局变量:{}\n'.format(name))
        del ENV[name]

    @staticmethod
    def loop_strategy(loop):
        """
        循环控制器策略
        """
        arr = np.array(loop)
        count = np.prod(arr)
        return count

    @staticmethod
    def skip_strategy(condition):
        """
        if控制器策略
        """

        tag = [_condition['condition'] for _condition in condition]
        if False not in tag:
            return True
        else:
            return False

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
        # 数据提取
        self.data_extraction(response.json(), data)
        # 断言
        checks = data.get('validators')
        self.validators(response.json(), checks)
        # 执行后置脚本
        self.__run_teardown_script(response)

    def perform(self, data):
        """一键压测扩展"""
        router = data.get('interface').get('url')
        threads = data.get('threads', 1)
        iterations = data.get('iterations', 1)
        http_sampler = HttpSampler(
            "Demo",
            router,
        )
        tg = ThreadGroupSimple(
            threads, iterations, http_sampler,
        )
        tp = TestPlan(tg)
        stats = tp.run()
        response = {
            "duration": stats.duration_milliseconds,
            "mean": stats.sample_time_mean_milliseconds,
            "min": stats.sample_time_min_milliseconds,
            "median": stats.sample_time_median_milliseconds,
            "90p": stats.sample_time_90_percentile_milliseconds,
            "95p": stats.sample_time_95_percentile_milliseconds,
            "99p": stats.sample_time_99_percentile_milliseconds,
            "max": stats.sample_time_max_milliseconds
        }
        self.__unittest_perform_response = response

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
        self.info_log('♾️当前运行环境\n',
                      "临时变量：{}\n".format(''.join(self.l_env)),
                      "全局变量：{}\n".format(''.join(self.g_env)))

    def __request_log(self) -> None:
        """请求信息日志输出"""
        self.debug_log("⚠️请求头：{}\n".format(self.requests_header))
        self.debug_log("⚠️请求体：{}\n".format(self.requests_body))
        self.debug_log("⚠️响应头：{}\n".format(self.response_header))
        self.debug_log("⚠️响应体：{}\n".format(self.response_body))
        self.info_log('⚠️请求响应状态码:{}\n'.format(self.status_code))

    def __send_request(self, data) -> Response:
        """发送请求"""
        request_info = self.__handler_request_data(data)
        self.info_log('⚠️发送请求[{}]:{}：\n'.format(request_info['method'].upper(), request_info['url']))
        try:
            response = session.request(**request_info)
        except Exception as e:
            raise ValueError('❌请求发送失败，错误信息如下：{}'.format(e))
        self.url = response.request.url
        self.method = response.request.method
        self.status_code = response.status_code

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
        # request_params['url'] = data.get('host') or ENV.get('host') + data.get('interface').get('url')
        if ENV.get('host'):
            request_params['url'] = ENV.get('host') + data.get('interface').get('url')
        else:
            request_params['url'] = data.get('interface').get('url')

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
                    raise ValueError('❌变量引用错误:\n{}中的变量{},在当前运行环境中未找到'.format(data, attr))
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
                    raise ValueError('❌变量引用错误：\n{}\n中的变量{},在当前运行环境中未找到'.format(
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

    def json_extract(self, obj, ext) -> Any:
        """jsonpath数据提取"""
        self.info_log('✴️jsonpath提取数据\n')
        value = jsonpath(obj, ext)
        value = value[0] if value else ''
        self.info_log('✴️提取表达式：{}\n'.format(ext), '提取结果:{}\n'.format(value))
        return value

    def re_extract(self, string, ext) -> Any:
        """正则表达式提取数据提取"""
        self.info_log('✴️正则提取数据\n')
        value = re.search(ext, string)
        value = value.group(1) if value else ''
        self.info_log('✴️提取表达式：{}\n'.format(ext), '提取结果:{}\n'.format(value))
        return value

    def data_extraction(self, response, case):
        """
        数据提取
        :param response: response对象
        :param case: 要提数据的数据，列表嵌套字典
        :return:
        """
        exts = case.get('extract') or getattr(self, 'extract', None)  # noqa
        if not (isinstance(exts, dict) and exts): return
        self.info_log("✴️从响应结果中开始提取数据\n")
        self.extras = []
        # 遍历要提取的数据
        for name, ext in exts.items():
            # 判断提取数据的方式
            if len(ext) == 3 and ext[1] == "jsonpath":
                value = self.json_extract(response, ext[2])
            elif len(ext) == 3 and ext[1] == "re":
                value = self.re_extract(response, ext[2])
            else:
                self.error_log("✴️变量{},的提取表达式 :{}格式不对！\n".format(name, ext))
                self.extras.append((name, ext, '提取失败！'))
                break
            if ext[0] == 'ENV':
                ENV[name] = value
            elif ext[0] == 'env':
                self.env[name] = value
            else:
                self.error_log("❌错误的变量级别，变量提取表达式中的变量级别只能为ENV，或者env\n".format(ext[1]))
                continue
            self.extras.append((name, ext, value))
            self.info_log("✴️提取变量：{},提取方式【{}】,提取表达式:{},提取值为:{}\n".format(name, ext[1], ext[2], value))

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
        self.info_log('*️⃣断言方法:{} 预期结果:{} 实际结果:{}\n'.format(methods, expected, actual))
        assert_method = methods_map.get(methods)
        global result # noqa
        if assert_method:
            try:
                assert_method(expected, actual)
            except Exception as err:
                self.warning_log('❌断言失败!\n')
                self.save_validators(methods, expected, actual, '【❌】')
                raise self.failureException(err)
            else:
                self.info_log("✅断言通过!\n")
                self.save_validators(methods, expected, actual, '【✔】')
        else:
            raise TypeError('❌断言比较方法{},不支持!'.format(methods))

    def __run_script(ep, data) -> None:  # noqa
        print = ep.print  # noqa
        env = ep.env  # noqa
        setup_script = data.get('setup_script')
        if setup_script:
            try:
                exec(setup_script)
            except Exception as e:
                ep.error_log('❌前置脚本执行错误: {}\n'.format(e))
                delattr(ep, 'hook_gen')
                raise
        response = yield  # noqa
        teardown_script = data.get('teardown_script')
        if teardown_script:
            try:
                exec(teardown_script)
            except Exception as e:
                ep.error_log('❌后置脚本执行错误: {}\n'.format(e))
                raise
        yield

    def __run_teardown_script(self, response) -> None:
        """执行后置脚本"""
        self.info_log('✳️执行后置脚本\n')
        self.hook_gen.send(response)
        delattr(self, 'hook_gen')

    def __run_setup_script(self, data):
        """执行前置脚本"""
        self.info_log('✳️执行前置脚本\n')
        self.hook_gen = self.__run_script(data) # noqa
        next(self.hook_gen)  # noqa
