from requests import request


class PytestRunner(object):

    def __init__(self, raw, module):
        self.raw = raw
        self.module = module

    def run(self):
        for function_name, value in self.raw.items():

            def function_template(*args, **kwargs):
                for step_key, step_value in value.items():
                    if step_key == 'request':
                        res = request(**step_value)
                    else:
                        eval(step_key)(step_value)

            setattr(self.module, function_name, function_template)
