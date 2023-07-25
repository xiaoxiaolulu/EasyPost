import ast
from typing import Any
import jsonpath
from core.http_handler import HttpHandler
from data import (
    validator,
    super_builtins
)
from data.extract import extract_by_object
from data.render_template_obj import render_template_context


class PytestRunner(object):

    def __init__(self, raw, module):
        self.raw = raw
        self.module = module
        self.context = {}

    def run(self):
        self.context.update(__builtins__)  # noqa
        self.context.update(super_builtins.__dict__)
        teststeps = self.raw.get('teststeps', [])  # noqa

        def function_template(*args, **kwargs):

            response = None
            for step in teststeps:
                for step_key, step_value in step.items():

                    if step_key == 'request':

                        request_body = render_template_context(f'''{step_value}''', **self.context)
                        http_request = HttpHandler(ast.literal_eval(request_body))    # noqa
                        response = http_request.request()

                    if step_key == 'validate':
                        self.assert_response(response, step_value)

                    if step_key == "extract":
                        extract_collections = self.extract_to_result(response, step_value)
                        self.context.update(extract_collections)
                    else:
                        try:
                            eval(step_key)(step_value)
                        except (NameError, KeyError, ValueError, AttributeError):
                            continue

        setattr(self.module, str(self.module.__name__), function_template)

    @staticmethod
    def extract_to_result(response: Any, extract_values: dict) -> dict:

        extract_collections = {
            extract_key: extract_by_object(response, extract_value)[-1]
            for extract_key, extract_value in extract_values.items()
            if isinstance(extract_values, dict)
        }
        return extract_collections

    @staticmethod
    def assert_response(response, validate_check):

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
