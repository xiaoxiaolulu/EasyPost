import importlib
import time
import typing
from functools import wraps
from unittest import TestSuite
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
from typing import (
    Any,
    Callable
)
import requests
from jsonpath import jsonpath
from requests_toolbelt import MultipartEncoder
from api.emus.CaseBaseEnum import RunningTstCasesEnum
from api.events.registry import registry
from unitrunner.engine.env import (
    BaseEnv,
    DEBUG,
    session,
    ENV,
    db
)
from unitrunner.engine.log import CaseRunLog
from unitrunner.engine.runner import TestRunner
from unitrunner.models import step

try:
    global_func = importlib.import_module('global_func')
except ModuleNotFoundError:
    from unitrunner.builitin import functions as global_func


class BaseTest(unittest.TestCase, CaseRunLog):

    def timer(self, second) -> None:
        """
        Waits for a specified number of seconds.

        This function uses the `time.sleep()` function to suspend the execution of the current
         thread for the given number of seconds (`second`). It then logs a message indicating the delay.

        Args:
            self (object): The object instance (not explicitly used in this function).
            second: The number of seconds to wait.

        Returns:
            None
        """
        time.sleep(second)
        self.info_log('强制等待:{}秒\n'.format(second))

    @staticmethod
    def skipIf(_condition, cls, test_name):
        """
        Skips a test case conditionally based on a provided condition.

        This function takes a condition (`_condition`), a test class (`cls`), and a test name (`test_name`)as arguments.
        It attempts to mark the specified test case as skipped if the condition evaluates to True.

        Args:
            _condition: A function or expression that evaluates to True or False.
                        If True, the test case will be skipped.
            cls: The test class containing the test case.
            test_name: The name of the test case to potentially skip.

        Returns:
            The original test case (`test_item`).

        Raises:
            AttributeError: If the specified test case is not found in the class.
        """
        test_item = getattr(cls, test_name)

        try:
            if _condition:
                test_item.__unittest_skip__ = True
                test_item.__unittest_skip_why__ = 'Skip'
            return test_item

        except (AttributeError,):
            return test_item

    def loop(self, loop_obj, cls, test_name, new_test_func):
        """
        Creates multiple test cases with unique names by dynamically attaching a test function to a class.

        This function generates multiple test cases within a class by repeatedly attaching the same test function
        with a unique name based on a loop count. It's designed for creating multiple test cases with similar
        structure but different data or variations.

        Args:
            self (object): The object instance (not explicitly used in this function).
            loop_obj: An object representing the loop count (either a number or None).
            cls: The test class to which the test cases will be attached.
            test_name: The base name for the test cases (will be suffixed with tags).
            new_test_func: The test function to be attached as multiple test cases.

        Returns:
            None
        """

        count = 1 if loop_obj is None else loop_obj  # noqa
        for c in range(int(count)):
            tag = f'_NoLooP_' if loop_obj is None else f'_Loop_{c + 1}'
            setattr(cls, f"{test_name + tag}", new_test_func)
            self.info_log('用例第{}次循环\n'.format(c + 1))

    def save_env_variable(self, name, value) -> None:
        """
        Saves a value to an environment variable, prioritizing object-level variables in non-debug mode.

        This function stores the provided `value` in an environment variable named `name`. It chooses the environment
        to store the variable in based on the debugging mode (`DEBUG`):
            - In debug mode (`DEBUG` is True), it saves the value to the global environment (`ENV`).
            - In non-debug mode, it saves the value to the object's environment (`self.env`).

        Args:
            self (object): The object instance (holds `env` in non-debug mode).
            name (str): The name of the environment variable to save.
            value: The value to store in the environment variable.

        Returns:
            None
        """
        self.info_log('♾️设置临时变量 变量名:{} 变量值:{}\n'.format(name, value))
        if DEBUG:
            self.debug_log('提示调试模式运行,设置的临时变量均保存到全局变量中\n')
            ENV[name] = value
        else:
            self.env[name] = value

    def get_env_variable(self, name) -> str:
        """
        Retrieves the value of an environment variable, prioritizing object-level variables in non-debug mode.

        This function fetches the value of an environment variable named `name`. It selects the source of the variable
        based on the debugging mode (`DEBUG`):
            - In debug mode (`DEBUG` is True), it retrieves the value from the global environment (`ENV`).
            - In non-debug mode, it retrieves the value from the object's environment (`self.env`).

        Args:
            self (object): The object instance (holds `env` in non-debug mode).
            name (str): The name of the environment variable to retrieve.

        Returns:
            The value of the environment variable.
        """
        self.info_log('获取临时变量 变量名:{}\n'.format(name))
        if DEBUG:
            return ENV[name]
        else:
            return self.env[name]

    def get_pre_url(self) -> str:
        """
        Retrieves the pre-URL from the environment.

        This function fetches the value of the environment variable named `url` and returns it.

        Args:
            self (object): The object instance (not used in this function).

        Returns:
            The value of the environment variable `url`.
        """
        pre_url = self.get_env_variable('url')
        return pre_url

    def save_global_variable(self, name, value) -> None:
        """
           Saves a global variable to the environment.

           This function stores a value in a global variable identified by its name (`name`)
           in the environment (assumed to be stored in a global dictionary named `ENV`).
           It logs the saving process with an informational message before actually storing the value.

           Args:
               self (object): The object instance (not explicitly used in this function).
               name (str): The name of the global variable to save.
               value: The value to store in the global variable.

           Returns:
               None
        """
        self.info_log('设置全局变量 变量名:{} 变量值:{}\n'.format(name, value))
        ENV[name] = value

    def delete_env_variable(self, name) -> None:
        """
        Deletes an environment variable from the current object's environment.

        This function removes an environment variable identified by its name (`name`)
        from the environment associated with the current object (`self.env`).
        It logs the deletion with an informational message before actually removing the variable.

        Args:
            self (object): The object instance (which holds the `env` environment).
            name (str): The name of the environment variable to delete.

        Returns:
            None
        """
        self.info_log('删除临时变量:{}\n'.format(name, ))
        del self.env[name]

    def delete_global_variable(self, name) -> None:
        """
        Deletes a global variable from the environment.

        This function removes a global variable identified by its name (`name`) from the environment
        (likely stored in a global dictionary named `ENV`).

        It logs the deletion with an informational message before actually removing the variable.

        Args:
            self (object): The object instance.
            name (str): The name of the global variable to delete.

        Returns:
            None
        """
        self.info_log('删除全局变量:{}\n'.format(name))
        del ENV[name]

    @staticmethod
    def loop_strategy(loop) -> int:
        """
        Calculates the total number of iterations for a nested loop.

        This function takes a list of loop lengths (`loop`) and calculates the total number of iterations
        by multiplying the lengths together.

        Args:
            loop (list): A list of integers representing the lengths of each nested loop.

        Returns:
            int: The total number of iterations for the nested loop.
        """

        arr = np.array(loop)
        count = np.prod(arr)
        return count

    @staticmethod
    def skip_strategy(condition) -> bool:
        """
        Determines whether to skip execution based on a list of conditions.

        This function takes a list of conditions (`condition`) and evaluates them using a specific strategy.
        The current strategy is to skip execution only if ALL conditions evaluate to False.

        Args:
            condition (list): A list of dictionaries representing conditions. Each dictionary should have a
            'condition' key.

        Returns:
            bool: True if all conditions are False, False otherwise.
        """
        tag = [_condition['condition'] for _condition in condition]
        if False not in tag:
            return True
        else:
            return False

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the class-level environment before running any tests in the class.

        This method is called once at the beginning of the test class execution.
        It performs the following tasks:
            - Initializes a base environment (`cls.env`) using `BaseEnv`.
            - Creates a session object depending on the debug flag (`DEBUG`):
            - If `DEBUG` is True, it uses the provided `session` object (likely for mocking or specific configurations).
            - Otherwise, it creates a new `requests.Session` object for making HTTP requests during tests.
        """
        cls.env = BaseEnv()
        if DEBUG:
            cls.session = session
        else:
            cls.session = requests.Session()

    def step(self, data) -> None:
        """
        Executes a single test step.

        Args:
            data: Dictionary containing step-specific data.

        Returns: None
        """
        # 日志记录
        self.__run_log()
        # 数据库查询
        self.execute_sql(data.get('sql', None))
        # 强制等待
        sleep = data.get('timer', 0)
        self.timer(sleep)
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
        """
        Validates a response against a set of validation checks.

        This function takes a response object and a list of validation checks (`validate_check`).
        Each check specifies a method, expected value (using a JSONPath expression), and an actual value for comparison.
        The function performs the validation and calls the `assertion` method for handling results.

        Args:
            response (Any): The response object to validate.
            validate_check (list): A list of validation checks, where each check is a dictionary.
        """
        if isinstance(validate_check, list):
            for check in validate_check:
                methods = check.get('method', None)
                expect = check.get('expect', None)
                expect_result = self.json_extract(response, expect)
                actual = check.get('actual', None)
                self.assertion(methods, expect_result, actual)

    def __run_log(self) -> None:
        """
        Logs local and global environment variables for informational purposes.

        This function formats and logs both the object's local environment variables (`self.env`)
        and the global environment variables (`ENV`) to provide context for debugging or understanding.

        Returns:
            None
        """
        self.l_env = ['\t{}:{}\n'.format(k, repr(v)) for k, v in self.env.items()]
        self.g_env = ['\t{}:{}\n'.format(k, repr(v)) for k, v in ENV.items()]
        self.info_log('当前运行环境\n',
                      "临时变量：{}\n".format(''.join(self.l_env)),
                      "全局变量：{}\n".format(''.join(self.g_env)))

    def __request_log(self) -> None:
        """
        Logs detailed information about a completed HTTP request.

        This function logs various details about the request and response to aid debugging.

        Returns:
            None
        """
        self.debug_log("请求头：{}\n".format(self.requests_header))
        self.debug_log("请求体：{}\n".format(self.requests_body))
        self.debug_log("响应头：{}\n".format(self.response_header))
        self.debug_log("响应体：{}\n".format(self.response_body))
        self.info_log('请求响应状态码:{}\n'.format(self.status_code))

    def none_connect_obj(self) -> dict[str, Callable[[Any], Any] | Callable[[Any], Any]]:
        """
        Creates and returns a dictionary representing a placeholder object
        used when a database connection cannot be established.

        This dictionary provides methods that mimic the behavior of the
        actual database connection methods but log an error message instead.

        Returns:
            A dictionary containing placeholder methods for commonly used
            database operations.
        """
        none_obj = {
            "query_sql": lambda x: self.error_log("❌MYSQL_HOST not found in config.py"),
            "execute_sql": lambda x: self.error_log("❌MYSQL_HOST not found in config.py")
        }
        return none_obj

    def execute_sql(self, sql: Any) -> typing.Union[dict, object]:
        """
        Executes a provided SQL query string and returns the results or a placeholder object on failure.

        Args:
            self: The object instance (likely related to database interaction).
            sql: The SQL query string to be executed.

        Returns:
            A dictionary containing the query results on success, or a placeholder object
            indicating a connection or execution failure.
        """
        try:
            setting = ENV.get('db') if self.env.get('db') is None else self.env.get('db')
            none_obj = self.none_connect_obj()

            setting_obj = type('Setting', (object,), setting)
            if not hasattr(setting_obj, 'database'):
                return none_obj
            try:
                database = db(setting)
                query_sql = {
                    "query_sql": database.execute(sql)
                }
                ENV.update(query_sql)
                return query_sql
            except Exception as err:
                self.error_log(f"❌Mysql Not connected {err}")
                return none_obj
        except (Exception,):
            pass

    def __send_request(self, data) -> Response:
        """
        Sends an HTTP request and handles the response.

        This function takes request data (`data`) as input, preprocesses it using `__handler_request_data`,
        sends the request using the `session` object, and processes the response.

        Args:
            data (dict): The request data dictionary containing various options.

        Returns:
            Response: The HTTP response object.
        """
        request_info = self.__handler_request_data(data)
        self.info_log('发送请求[{}]:{}：\n'.format(request_info['method'].upper(), request_info['url']))
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
        """
        Preprocesses request data for an outgoing HTTP request.

        This function takes request data (`data`) as input and performs various transformations
        to prepare it for making an HTTP request.

        Args:
            data (dict): The request data dictionary containing various options.

        Returns:
            dict[str | Any, Any]: The preprocessed request data dictionary, ready for making an HTTP request.
        """
        if ENV.get('headers'):
            data['headers'] = ENV.get('headers').update(data.get('headers'))

        for k, v in list(data.items()):
            if k not in ['setup_script', "run_teardown_script"]:
                v = self.__parser_variable(v)
                data[k] = v

        files = data.get('files')
        if files:
            if isinstance(files, dict):
                file_data = files.items()
            else:
                file_data = files
            field = []
            for name, file_info in file_data:

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

        request_params = {}

        params_fields = ['url', 'method', 'params', 'data', 'json', 'files', 'headers', 'cookies', 'auth', 'timeout',
                         'allow_redirects', 'proxies', 'hooks', 'stream', 'verify', 'cert']
        for k, v in data['request'].items():
            if k in params_fields:
                request_params[k] = v

        # request_params['url'] = data.get('host') or ENV.get('host') + data.get('interface').get('url')
        if ENV.get('host'):
            request_params['url'] = ENV.get('host') + data.get('interface').get('url')
        else:
            request_params['url'] = data.get('interface').get('url')

        request_params['method'] = data.get('interface').get('method')
        request_params['headers'] = data['headers']
        return request_params

    def __parser_variable(self, data) -> str | None | Any:
        """
        Parses variables in a string, list, or dictionary, replacing them with values from environments.

        Variables are in the format `${variable_name}`. Environment values are retrieved from either a global
        `ENV` dictionary or the object's `env` dictionary.

        Args:
            data: The data to parse, which can be a string, list, or dictionary.

        Returns:
            str | None | Any: The parsed data, type depending on input data:
                - String: The parsed string with variables replaced.
                - List or Dictionary: The equivalent parsed list or dictionary.
                - None: If the input data is of an unsupported type.
        """
        pattern = r'\${{(.+?)}}'
        old_data = data

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
        """
        Extracts a value from a JSON object using a JSONPath expression.

        This method uses the `jsonpath` library (assumed to be installed) to extract data from a JSON object (`obj`)
        based on the provided JSONPath expression (`ext`).

        Args:
            obj (dict): The JSON object to extract data from.
            ext (str): The JSONPath expression specifying the path to the desired value.

        Returns:
            Any: The extracted value if found, otherwise an empty string.
        """
        self.info_log('jsonpath提取数据\n')
        value = jsonpath(obj, ext)
        value = value[0] if value else ''
        self.info_log('提取表达式：{}\n'.format(ext), '提取结果:{}\n'.format(value))
        return value

    def re_extract(self, string, ext) -> Any:
        """
        Extracts a value from a string using a regular expression.

        This method attempts to find a match for the provided regular expression (`ext`) within the given `string`.

        Args:
            string (str): The string to search for the pattern.
            ext (str): The regular expression pattern to use for extraction.

        Returns:
            Any: The extracted value if a match is found, otherwise an empty string.
        """
        self.info_log('正则提取数据\n')
        value = re.search(ext, string)
        value = value.group(1) if value else ''
        self.info_log('提取表达式：{}\n'.format(ext), '提取结果:{}\n'.format(value))
        return value

    def data_extraction(self, response, case):
        """
        Extracts data from a response object based on a list of JSONPath expressions.

        This function takes a response object (`response`) and a list of JSONPath expressions (`case`) as input.
        It uses the `jsonpath_rw` library to extract the data from the response and returns the results.

        Args:
            response (Any): The response object to extract data from.
            case (Any): A list of JSONPath expressions representing the data to be extracted.

        Returns:
            Any: The extracted data.
        """
        exts = case.get('extract') or getattr(self, 'extract', None)  # noqa
        if not (isinstance(exts, dict) and exts): return
        self.info_log("从响应结果中开始提取数据\n")
        self.extras = []
        # 遍历要提取的数据
        for name, ext in exts.items():
            # 判断提取数据的方式
            if len(ext) == 3 and ext[1] == RunningTstCasesEnum.EXTRACT_JSON_PATH:
                value = self.json_extract(response, ext[2])
            elif len(ext) == 3 and ext[1] == RunningTstCasesEnum.EXTRACT_RE:
                value = self.re_extract(response, ext[2])
            else:
                self.error_log("变量{},的提取表达式 :{}格式不对！\n".format(name, ext))
                self.extras.append((name, ext, '提取失败！'))
                break
            if ext[0] == RunningTstCasesEnum.ENV_BIG:
                ENV[name] = value
            elif ext[0] == RunningTstCasesEnum.ENV_LITTLE:
                self.env[name] = value
            else:
                self.error_log("❌错误的变量级别，变量提取表达式中的变量级别只能为ENV，或者env\n".format(ext[1]))
                continue
            self.extras.append((name, ext, value))
            self.info_log("✴️提取变量：{},提取方式【{}】,提取表达式:{},提取值为:{}\n".format(name, ext[1], ext[2], value))

    def assertion(self, methods, expected, actual) -> None:
        """
        Performs an assertion based on the provided method and validates the results.

        This function takes the assertion method name (`methods`), expected value, and actual value as input.
        It retrieves the corresponding assertion method using `self.get_assert_method()`, performs the assertion,
        and handles both successful and failed assertions with logging and result recording.

        Args:
            self (object): The object instance.
            methods (str): The name of the assertion method to use.
            expected (Any): The expected value for the assertion.
            actual (Any): The actual value to be compared against.

        Returns:
            None
        """

        self.info_log('断言方法:{} 预期结果:{} 实际结果:{}\n'.format(methods, expected, actual))
        assert_method = registry.get(methods)
        global result  # noqa
        if assert_method:
            try:
                assert_method(expected, actual)
            except Exception as err:
                self.warning_log('❌断言失败!\n')
                self.save_validators(methods, expected, actual, '【❌】')
                raise self.failureException(err)
            else:
                self.info_log("断言通过!\n")
                self.save_validators(methods, expected, actual, '【✔】')
        else:
            raise TypeError('❌断言比较方法{},不支持!'.format(methods))

    def __run_script(ep, data) -> None:  # noqa
        """
            Executes a script within an execution context (ep) with access to environment and print function.

            This method likely operates within the context of a test runner or similar framework.
            It takes an execution point (ep) object and script data (`data`) as arguments.

            Args:
                ep: The execution point object (assumed to provide environment and printing functionality).
                data (dict): The script data dictionary containing potential setup and teardown script information.

            Yields:
                Any: The data yielded by the script execution (if applicable).
            """
        print = ep.print  # noqa
        env = ep.env  # noqa
        setup_script = data.get('setup_script', '')
        if setup_script:
            try:
                exec(setup_script)
            except Exception as e:
                ep.error_log('❌前置脚本执行错误: {}\n'.format(e))
                delattr(ep, 'hook_gen')
                raise

        response = yield  # noqa
        teardown_script = data.get('teardown_script', '')
        if teardown_script:
            try:
                exec(teardown_script)
            except Exception as e:
                ep.error_log('❌后置脚本执行错误: {}\n'.format(e))
                raise
        yield

    def __run_teardown_script(self, response) -> None:
        """
        Executes a teardown script and sends the test response.

        This method likely performs the following steps:

        1. Logging: Logs a blank line for potential formatting purposes.
        2. Generator Interaction: Assumes a generator object (`self.hook_gen`) exists from a previous setup script execution.
           - Sends the `response` data to the generator using the `send` method.
           - The generator might process the response data or perform cleanup actions.
        3. Cleanup: Deletes the `hook_gen` attribute to avoid memory leaks or unintended references.

        Args:
            response (Any): The response data from the test execution.

        Returns:
            None
        """
        self.info_log('执行后置脚本\n')
        self.hook_gen.send(response)
        delattr(self, 'hook_gen')

    def __run_setup_script(self, data):
        """
        Executes a setup script and iterates through its generator.

        This method likely performs the following steps:

        1. Logging: Logs a blank line for potential formatting purposes.
        2. Script Execution: Calls the `__run_script` method (assumed to be defined within the class)
           to execute the setup script and capture the returned generator object.
        3. Generator Initialization: Starts the execution of the generator by calling `next` on it.
           The generator likely yields data or performs actions step-by-step.

        Args:
            data: The data for the setup script.

        Yields:
            Any: The data yielded by the `__run_script` generator (if applicable).
        """
        self.info_log('执行前置脚本\n')
        self.hook_gen = self.__run_script(data)  # noqa
        next(self.hook_gen)  # noqa


class GenerateCase:

    def __init__(self):
        self.controller = BaseTest()

    def data_to_suite(self, datas: step.TestCase) -> TestSuite:
        """
        Converts test case data into a unittest.TestSuite object.

        This method takes test case data (`datas`) and transforms it into a `TestSuite`
        suitable for running with the `unittest` framework. It handles two main cases:

        1. List of test case definitions:
            - If `datas` is a list, it iterates through each item (assumed to be a test case definition dictionary).
            - For each item, it calls `add_test` to create a test class or add a single test case to the `suite`.

        2. Single test case definition:
            - If `datas` is a dictionary, it directly treats it as a single test case definition.
            - It calls `add_test` to create a test class or add the single test case to the `suite`.

        Args:
            datas (step.TestCase | list[step.TestCase]): The test case data in the format of a single TestCase object
                                                        or a list of TestCase objects.

        Returns:
            TestSuite: The constructed TestSuite object containing the tests.
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
        """
        Adds a test class or a single test case to a test suite.

        This method processes a test case definition (`item`) and a test loader (`load`).
        It creates a corresponding test class using `create_test_class` and then adds the tests
        to the provided `suite`.

        Args:
            item (dict): The test case definition dictionary containing information about the class or single test case.
            load (TestSuiteLoader): An instance of `TestSuiteLoader` (assumed) for loading tests from classes.
            suite (TestSuite): The test suite object where tests will be added.
        """

        cls = self.create_test_class(item)
        suite.addTest(load.loadTestsFromTestCase(cls))  # noqa

    def create_test_class(self, item) -> type:
        """
        Creates a dynamic test class from a test case definition.

        This method takes a test case definition (`item`) dictionary and generates a corresponding test class.

        Args:
            item (dict): The test case definition dictionary containing information about the class and its test cases.

        Returns:
            type: The newly created test class derived from `BaseTest`.
        """

        # Extract class name or set a default
        cls_name = item.get('name') or 'Demo'

        # Extract test cases or use the entire item if no cases provided
        cases = item.get('cases', None)
        collections = cases if cases is not None else [item]

        # Create the class dynamically
        cls = type(cls_name, (BaseTest,), {})

        # Process test cases and generate test functions within the class
        self.create_case_content(cls, collections)

        # Return the newly created test class
        return cls

    def create_case_content(self, cls, cases, skip_collections: list = [], loop_collections: list = []):
        """
        Recursively processes test cases and generates corresponding test functions.

        This method iterates through a list of test cases (`cases`) and performs the following actions:

        Args:
            cls (class): The class where test functions will be added.
            cases (list): A list of test case data dictionaries.
            skip_collections (list, optional): List to accumulate `If` conditions for skipping (defaults to []).
            loop_collections (list, optional): List to accumulate `Loop` counts for looping (defaults to []).

        """

        for index, case_ in enumerate(cases):
            mode = case_.get('mode', 'normal')

            if mode == RunningTstCasesEnum.MODE:
                global children  # noqa
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

                    loop_count = self.controller.loop_strategy(loop_collections)
                    if_object = self.controller.skip_strategy(skip_collections)

                    test_name = self.create_test_name(index, len(cases))
                    new_test_func = self.create_test_func(getattr(cls, 'step'), case_)
                    new_test_func.__doc__ = case_.get('title') or new_test_func.__doc__

                    self.controller.loop(loop_count, cls, test_name, new_test_func)

                    test_name = [name for name in cls.__dict__.keys() if name.__contains__('test_')]

                    self.controller.skipIf(if_object, cls, str(test_name.pop()))

            else:

                test_name = self.create_test_name(index, len(cases))
                new_test_func = self.create_test_func(getattr(cls, 'perform'), case_)
                new_test_func.__doc__ = case_.get('title') or new_test_func.__doc__
                setattr(cls, test_name, new_test_func)

    def create_test_func(self, func, case_) -> Callable[[Any], None]:
        """
        Creates a wrapper function for a test case.

        This method generates a new function that wraps around the provided `func`
        and injects the `case_` argument during execution. It uses the `wraps` decorator
        from the `functools` module (assumed to be imported) to preserve the original
        function's metadata (like name, docstring).

        Args:
            self (object): The instance of the class to which the wrapper belongs (likely a test runner).
            func (Callable[[Any], Any]): The original test function to be wrapped.
            case_ (Any): The test case data that will be passed to the wrapped function.

        Returns:
            Callable[[Any], None]: The generated wrapper function that executes the original
                                    function with the provided test case data.
        """

        @wraps(func)
        def wrapper(self):  # noqa
            """Wrapper function for the test case"""
            func(self, case_)

        return wrapper

    @staticmethod
    def create_test_name(index: int, length: int) -> str:
        """
        Generates a test name with a specific format.

        This static method constructs a test name string following a pattern of "test_"
        padded with zeros and appended with a sequential index (starting from 1).
        The number of leading zeros is determined based on the provided `length` parameter.

        Args:
            index (int): The index for the test case (starting from 1).
            length (int): The desired total length of the test name (including zeros and index).

        Returns:
            str: The generated test name with the format "test_000N" where N is the index.
        """

        # Calculate the number of leading zeros to pad
        num_zeros = (len(str(length)) // len(str(index))) - 1

        # Format the test name with leading zeros and index
        test_name = 'test_{}'.format("0" * num_zeros + str(index + 1))

        return test_name


def run_test(case_data, env_config={}, tester='tester', thread_count=1, debug=True) -> tuple[Any, dict[
    Any, Any]] | Any:  # noqa
    """
      Executes the test suite.

      This function takes the test suite data (`case_data`), environment configuration (`env_config`),
      number of threads (`thread_count`), debug mode (`debug`), and tester name (`tester`) as input.
      It executes the test suite and returns the results.

      Args:
          case_data (Any): The test suite data.
          env_config (Any): The environment configuration for test case execution.
              env_config:{
              'ENV':{"host":'http//:127.0.0.1'},
              'db':[{},{}],
              'FuncTools':'工具函数文件'
              }
          thread_count (int): The number of threads to use for execution.
          debug (bool): Debug mode flag for single interface debugging.
          tester (str): The name of the tester.

      Returns:
          Any: In debug mode, returns the results of the current run and the global variables set for the current run.
    """
    global global_func, db, DEBUG, ENV, result  # noqa
    global_func_file = env_config.get('global_func', b'')
    if global_func_file:
        with open('global_func.py', 'w', encoding='utf-8') as f:
            f.write(global_func_file)  # noqa

    global_func = importlib.reload(global_func)
    DEBUG = debug
    ENV = {**env_config.get('ENV', {})}
    db.init_connect(env_config.get('db', []))
    rerun = env_config.get('rerun', 0)
    suite = GenerateCase().data_to_suite(case_data)
    runner = TestRunner(suite=suite, tester=tester)
    result = runner.run(thread_count=thread_count, rerun=rerun)
    if global_func and global_func_file:
        os.remove('global_func.py')
    db.close_connect()
    return result


def run_api(api_data: dict, tester: str = 'tester', thread_count: int = 1) -> tuple[Any, dict[Any, Any]] | Any:  # noqa
    """
    Runs a single API interface test.

    This function takes API data as a dictionary, an optional tester name (defaults to 'tester'),
    and an optional thread count (defaults to 1) for concurrent execution. It performs the following steps:

    1. Generates test cases: Uses an instance of `GenerateCase` (assumed to be a class
       responsible for test case generation) to convert the API data into a test suite.
    2. Runs test cases: Creates a `TestRunner` instance (assumed to be a class for running tests)
       and executes the generated test suite with the provided tester name and thread count.
    3. Closes database connection: Closes the database connection (assuming `db.close_connect`
       is a function for closing the database connection).
    4. Returns result: Returns the test result and a report dictionary (structure depends on the implementation
       of `TestRunner.run`).

    Args:
        api_data (dict): Dictionary containing data for the API interface.
        tester (str, optional): Name of the tester running the test (defaults to 'tester').
        thread_count (int, optional): Number of threads for concurrent execution (defaults to 1).

    Returns:
        tuple[Any, dict[Any, Any]] | Any: A tuple containing the test result (type depends on the
        implementation of `TestRunner.run`) and a dictionary holding the test report data
        (structure depends on the implementation of `TestRunner.run`).
    """

    suite = GenerateCase().data_to_suite(api_data)
    runner = TestRunner(suite=suite, tester=tester)
    result = runner.run(thread_count=thread_count)
    db.close_connect()
    return result
