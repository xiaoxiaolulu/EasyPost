import jsonpath
from core.http_handler import HttpHandler
from data.validator import equal


class PytestRunner(object):

    def __init__(self, raw, module):
        self.raw = raw
        self.module = module

    def run(self):
        for function_name, value in self.raw.items():

            def function_template(*args, **kwargs):

                response = None
                for step_key, step_value in value.items():
                    if step_key == 'request':

                        http_request = HttpHandler(step_value)
                        response = http_request.request()
                    if step_key == 'validate':
                        self.assert_response(response, step_value)
                    else:
                        try:
                            eval(step_key)(step_value)
                        except NameError:
                            continue
            setattr(self.module, function_name, function_template)

    @staticmethod
    def assert_response(response, validate_check):

        for check in validate_check:
            for check_type, check_value in dict(check).items():
                if check_type in ["eq", "equal"]:
                    yaml_result = check_value[0]
                    actual_result = jsonpath.jsonpath(response, yaml_result).pop()
                    expect_result = check_value[1]
                    equal(expect_result, actual_result)
