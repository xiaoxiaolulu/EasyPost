import ast
import copy
import json
import pathlib
from inspect import Parameter
from typing import (
    Any,
    Callable,
    List
)
import jsonpath
import yaml
from requests_toolbelt import MultipartEncoder
from config.settings import (
    BASE_DIR,
    DATABASES
)
from core.request.create_function import create_function_from_parameters
from core.request.http_handler import HttpHandler
from core.request import validator
from utils import super_builtins
from core.request.extract import extract_by_object
from utils.db import OperateMysql
from utils.log import log
from utils.render_template_obj import *


class PytestRunner(object):

    def __init__(self, raw, module):
        self.raw = raw
        self.module = module
        self.context = {}

    def run(self):
        self.context.update(__builtins__)  # noqa
        self.context.update(super_builtins.__dict__)
        self.context.update(**self.execute_sql())
        teststeps = self.raw.get('teststeps', [])  # noqa
        fixtures = self.raw.get('config').get('fixtures', [])
        params = self.raw.get('config').get('parameters', [])
        config_fixtures, config_params = self.parameters(fixtures, params)

        def function_template(*args):

            log.info(f'执行文件-> {self.module.__name__}.yaml')

            response = None
            for index, step in enumerate(teststeps):
                for step_key, step_value in step.items():

                    if step_key == "name":
                        log.info(f'用例步骤：{index + 1} -> {step_value}')

                    if step_key == 'api':
                        api_root = pathlib.Path(BASE_DIR).joinpath(step_value)
                        raw_dict = yaml.safe_load(api_root.open(encoding='utf-8'))
                        copy_value = copy.deepcopy(raw_dict.get('request'))
                        response = self.run_request(args, copy_value, self.context)

                    if step_key == 'request':
                        response = self.run_request(args, step_value, self.context)

                    if step_key == 'validate':
                        log.info(f'断言 -> {step_value}')
                        self.assert_response(response, step_value)

                    if step_key == "extract":
                        extract_collections = self.extract_to_result(response, step_value)
                        self.context.update(extract_collections)

                        log.info('参数提取 -> {}'.format(
                            json.dumps(extract_collections, indent=4, ensure_ascii=False)
                        ))
                    else:
                        try:
                            eval(step_key)(step_value)
                        except (NameError, KeyError, ValueError, AttributeError):
                            continue

        f = create_function_from_parameters(
            func=function_template,
            parameters=self.fixture_parameters(config_fixtures),
            documentation=self.module.__name__,
            func_name=self.module.__name__,
            func_filename=f"{self.module.__name__}.py",
        )

        setattr(self.module, str(self.module.__name__), f)

        if config_params:
            setattr(self.module, 'params_data', config_params)

    def execute_sql(self) -> dict[str, Callable[[Any], Any] | Callable[[Any], Any]] | dict[
        str, Callable[[tuple[Any, ...], dict[str, Any]], None | tuple[Any, ...] | tuple[tuple[Any, ...], ...]]]:  # noqa
        setting = DATABASES.get("default")
        none_obj = self.none_connect_obj()

        setting_obj = type('Setting', (object,), setting)
        if not hasattr(setting_obj, 'database'):
            return none_obj
        try:
            db = OperateMysql(setting)
            return {
                "query_sql": db.execute
            }
        except Exception as err:
            log.error(f"Mysql Not connected {err}")
            return none_obj

    @staticmethod
    def none_connect_obj() -> dict[str, Callable[[Any], Any] | Callable[[Any], Any]]:
        none_obj = {
            "query_sql": lambda x: log.error("MYSQL_HOST not found in config.py"),
            "execute_sql": lambda x: log.error("MYSQL_HOST not found in config.py")
        }
        return none_obj

    @staticmethod
    def fixture_parameters(config_fixtures: str) -> list[Parameter]:

        fixture_collections = [
            Parameter('request', Parameter.POSITIONAL_OR_KEYWORD)
        ]
        for fixture in config_fixtures:
            if fixture not in ['requests_function', 'requests_module']:
                fixture_collections.append(
                    Parameter(fixture, Parameter.POSITIONAL_OR_KEYWORD),
                )
        return fixture_collections

    @staticmethod
    def parameters(fixtures: str, parameters: List[List[Any]]) -> tuple[list[str], list[list[Any]]] | tuple[
        list[str], list[Any]]:  # noqa
        """
        "fixtures": "username, password",
        "parameters": [["test1", "123456"], ["test2", "123456"]]:
        """

        if isinstance(fixtures, str):
            fixtures = [item.strip() for item in fixtures.split(',')]

        if isinstance(parameters, list) and len(parameters) > 1:
            parameters_collections = fixtures, parameters
        else:
            parameters_collections = fixtures, []

        return parameters_collections

    def run_request(self, args, request_body: dict, ctx: dict) -> Any:
        self.context.update(args[0])
        request_body = render_template_context(f'''{request_body}''', **ctx)
        request_body = ast.literal_eval(request_body)
        request_body = self.multipart_encoder_request(request_body)

        log.info(
            f"--------  request info ----------\n"
            "{}".format(json.dumps(request_body, indent=4, ensure_ascii=False))
        )

        http_request = HttpHandler(request_body)  # noqa
        response = http_request.request()

        log.info(
            f"--------  response info ----------\n"
            f"status: {response.get('status')}\n"
            f"msg: {response.get('msg')}\n"
            f"statusCode: {response.get('statusCode')}\n"
            f"responseHeaders:\n"
            f"{json.dumps(response.get('responseHeaders'), indent=4, ensure_ascii=False)}\n"
            f"responseBody:\n"
            f"{json.dumps(response.get('responseBody'), indent=4, ensure_ascii=False)}\n"
            f"cookies: {response.get('cookies')}\n"
            f"cost: {response.get('cost')}\n"
            f"cookie: {response.get('cookie')}"
        )
        return response

    @staticmethod
    def multipart_encoder_request(request_body):
        """
        FIXME  测试地址 http://httpbin.org/post
        """

        if 'files' in request_body.keys():

            for key, value in request_body.get('files', {}).items():
                if pathlib.Path(BASE_DIR).joinpath(value).is_file():
                    with open(pathlib.Path(BASE_DIR).joinpath(value), 'rb') as f:
                        encoder = MultipartEncoder(fields={'file': ('filename', f)})

            request_body.pop('files')
            request_body['data'] = encoder
            new_headers = request_body.get('headers', {})
            new_headers.update({'Content-Type': encoder.content_type})
            request_body['headers'] = new_headers

            return request_body
        else:
            return request_body

    @staticmethod
    def extract_to_result(response: Any, extract_values: dict) -> dict:

        extract_collections = {
            extract_key: extract_by_object(response, extract_value)[-1]
            for extract_key, extract_value in extract_values.items()
            if isinstance(extract_values, dict)
        }
        return extract_collections

    @staticmethod
    def assert_response(response: Any, validate_check: List[dict[Any]]) -> None:

        for check in validate_check:
            for check_type, check_value in dict(check).items():

                yaml_result = check_value[0]
                actual_result = jsonpath.jsonpath(response, yaml_result).pop()
                expect_result = check_value[1]

                if check_type in ["eq", "equal"]:
                    validator.assert_equal(expect_result, actual_result)
                if check_type in ["ne", "not_equal"]:
                    validator.assert_not_equal(expect_result, actual_result)
                if check_type in ["in", "contain", "contains"]:
                    validator.assert_in(expect_result, actual_result)
                if check_type in ["ni", "not_in", "not_contain"]:
                    validator.assert_not_in(expect_result, actual_result)
                if check_type in ["is"]:
                    validator.assert_is(expect_result, actual_result)
                if check_type in ["in", "is_not"]:
                    validator.assert_is_not(expect_result, actual_result)
                if check_type in ["ec", "equal_count"]:
                    validator.assert_equal_count(expect_result, actual_result)
                if check_type in ["gt", "greater"]:
                    validator.assert_greater(expect_result, actual_result)
                if check_type in ["ge", "greater_equal"]:
                    validator.assert_greater_equal(expect_result, actual_result)
                if check_type in ["le", "less_equal"]:
                    validator.assert_less_equal(expect_result, actual_result)
                if check_type in ["le", "less"]:
                    validator.assert_less(expect_result, actual_result)
