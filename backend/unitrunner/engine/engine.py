import ast
import copy
import inspect
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
from unitrunner import exceptions
from unitrunner.constructor.create_function import create_function_from_parameters
from unitrunner.builitin import compares
from unitrunner.engine.extract import extract_by_object
from unitrunner.database.db import OperateMysql
from utils.logger import log
from utils.render_template_obj import *


class PytestRunner(object):

    def __init__(self, raw, module):
        self.raw = raw
        self.module = module
        self.context = {}

    def run(self):
        self.context.update(__builtins__)  # noqa
        # self.context.update(builtin.__dict__) # noqa
        self.context.update(**self.execute_sql())
        teststeps = self.raw.get('teststeps', [])  # noqa
        fixtures = self.raw.get('config', {}).get('fixtures', [])
        params = self.raw.get('config', {}).get('parameters', [])
        config_fixtures, config_params = self.parameters(fixtures, params)

        def function_template(*args):

            log.info(f'🔅执行文件-> {self.module.__name__}.yaml')
            log.info(f'🔅参数化数据-> {self.ass_parameters(fixtures, params)}')

            response = None
            for index, step in enumerate(teststeps):
                for step_key, step_value in step.items():

                    if step_key == "name":
                        log.info(f'🔅用例步骤：{index + 1} -> {step_value}')

                    if step_key == 'api':
                        api_root = pathlib.Path(BASE_DIR).joinpath(step_value)
                        raw_dict = yaml.safe_load(api_root.open(encoding='utf-8'))
                        copy_value = copy.deepcopy(raw_dict.get('request', {}))
                        response = self.run_request(args, copy_value, self.context)

                    if step_key == 'request':
                        response = self.run_request(args, step_value, self.context)

                    if step_key == 'validate':
                        log.info(f'断言 -> {step_value}')
                        self.assert_response(response, step_value)

                    if step_key == "extract":
                        extract_collections = self.extract_to_result(response, step_value)
                        self.context.update(extract_collections)

                        log.info('🔅参数提取 -> {}'.format(
                            json.dumps(extract_collections, indent=4, ensure_ascii=False)
                        ))
                    else:
                        try:
                            eval(step_key)(step_value)
                        except exceptions.StepRuntimeError:
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
        setting = DATABASES.get("default", {})
        none_obj = self.none_connect_obj()

        setting_obj = type('Setting', (object,), setting)
        if not hasattr(setting_obj, 'database'):
            return none_obj
        try:
            db = OperateMysql(setting)
            return {
                "query_sql": db.execute
            }
        except exceptions.MysqlConnectionException as err:
            log.error(f"❌Mysql Not connected {err}")
            return none_obj

    @staticmethod
    def none_connect_obj() -> dict[str, Callable[[Any], Any] | Callable[[Any], Any]]:
        none_obj = {
            "query_sql": lambda x: log.error("❌MYSQL_HOST not found in config.py"),
            "execute_sql": lambda x: log.error("❌MYSQL_HOST not found in config.py")
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

    @staticmethod
    def ass_parameters(fixtures: str, parameters: List[List[Any]]) -> list[dict] | list[Any]:

        if isinstance(fixtures, str) and isinstance(parameters, list) and len(parameters) > 1:
            fixtures = [item.strip() for item in fixtures.split(',')]

            ass_params_collections = [{
                fixtures[index]: value
                for index, value in enumerate(param)
            } for param in parameters]

        else:
            ass_params_collections = []

        return ass_params_collections

    def run_request(self, args, request_body: dict, ctx: dict) -> Any:

        log.info(f"🔆当前用例引用参数化数据-> {args[0]}")

        self.context.update(args[0])
        request_body = render_template_context(f'''{request_body}''', **ctx)
        request_body = ast.literal_eval(request_body)
        request_body = self.multipart_encoder_request(request_body)

        log.info(
            f"--------  request info ----------\n"
            "{}".format(json.dumps(request_body, indent=4, ensure_ascii=False))
        )

        #  前置
        request_pre = request_body.get('hooks', {}).get('request_hooks', [])
        self.request_hooks(request_pre)
        log.info(
            "f--------  执行前置条件 ----------\n"
            "{}".format("".join(request_pre))
        )

        http_request = HttpHandler(request_body)  # noqa
        response = http_request.request()

        log.info(
            f"--------  response info ----------\n"
            f"status: {response.get('status', None)}\n"
            f"msg: {response.get('msg', None)}\n"
            f"statusCode: {response.get('statusCode', None)}\n"
            f"responseHeaders:\n"
            f"{json.dumps(response.get('responseHeaders', {}), indent=4, ensure_ascii=False)}\n"
            f"responseBody:\n"
            f"{json.dumps(response.get('responseBody', {}), indent=4, ensure_ascii=False)}\n"
            f"cookies: {response.get('cookies', None)}\n"
            f"cost: {response.get('cost', None)}\n"
            f"cookie: {response.get('cookie', None)}"
        )

        # 后置
        response_pos = request_body.get('hooks', {}).get('response_hooks', [])
        self.request_hooks(response_pos)
        log.info(
            "f--------  执行后置条件 ----------\n"
            "{}".format("".join(response_pos))
        )

        return response

    def request_hooks(self, request_pre: list) -> None:

        if isinstance(request_pre, list) and len(request_pre) >= 1:

            hook_args = None
            for pre in request_pre:

                func = self.context.get(pre, {})
                argsname = [argsname for argsname, value in inspect.signature(func).parameters.items()] # noqa
                if "request_args" in argsname:
                    args = self.context.get("request_args", {})
                    hook_args = func(args)

                else:
                    hook_args = func()

            self.context.update(hook_args) if hook_args is not None else None
        else:
            return None

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
