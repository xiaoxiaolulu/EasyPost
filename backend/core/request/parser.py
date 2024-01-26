import json
from typing import (
    List,
    Dict
)


class HandelTestData(object):

    def __init__(self, request_body: Dict = None) -> None:
        try:
            # 额外参数
            self.directory_id = request_body.get('directory_id', None)
            self.project = request_body.get('project', None)

            # 基本信息
            self.name = request_body.get('name', None)
            self.url = request_body.get('url', None)
            self.method = request_body.get('method', None)
            self.priority = request_body.get('priority', None)
            self.status = request_body.get('status', None)
            self.desc = request_body.get('desc', None)

            # 请求体
            self.headers = json.dumps(request_body.get('headers', []))
            self.raw = json.dumps(request_body.get('raw', {}))
            self.params = json.dumps(request_body.get('params', []))
            self.setup_script = request_body.get('setup_script', None)
            self.teardown_script = request_body.get('teardown_script', None)
            self.validate = json.dumps(request_body.get('validate', []))
            self.extract = json.dumps(request_body.get('extract', []))

            # 一键压测
            self.mode = request_body.get('mode', 'normal')
            self.threads = request_body.get('threads', 1)
            self.iterations = request_body.get('iterations', 1)

            # 步骤
            self.step_data = request_body.get('step_data', [])

            # 计划
            self.cron = request_body.get('cron', None)
            self.case_list = request_body.get('case_list', [])
            self.state = request_body.get('state', 0)
            self.pass_rate = request_body.get('pass_rate', '80%')
            self.msg_type = request_body.get('msg_type', 0)
            self.receiver = request_body.get('receiver', [])

        except (KeyError, ValueError, AttributeError):
            pass

    @staticmethod
    def resolve_headers(headers):
        """
        [{'name': 'Content-Type', 'value': 'application/json', 'description': '', 'edit': False}]

        "headers": {
            'content-Type': "application/json"
        },
        """
        headers = {item['name']: item['value'] for item in json.loads(headers)}
        return headers

    @staticmethod
    def resolve_form_data(raw):
        """
        {'data': [{'id': 912586, 'edit': False, 'visible': False, 'name': '33', 'value': '333', 'type': 'Integer', 'description': '33'}]}

        'data': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
        """
        form_data_items = eval(raw).get('form_data', [])
        form_data = {
            'data': {item['name']: item['value'] for item in form_data_items}
        }
        return form_data

    @staticmethod
    def resolve_x_www_form_urlencoded(raw):
        """
        {'data': [{'id': 912586, 'edit': False, 'visible': False, 'name': '33', 'value': '333', 'type': 'Integer', 'description': '33'}]}

        'data': {"mobile_phone": "${{user_mobile}}", "pwd": "llll"},
        """
        form_data_items = eval(raw).get('x_www_form_urlencoded', [])
        form_data = {
            'data': {item['name']: item['value'] for item in form_data_items}
        }
        return form_data

    @staticmethod
    def resolve_json(raw):
        """
        {'json': '{"$schema": "http://json-schema.org/draft-04/schema"}'}
        """
        json_items = eval(raw).get('json', [])
        json_data = {
            'json': json.loads(json_items)
        }
        return json_data

    def raw_conversion(self, raw):

        json_target = eval(raw).get('json', [])
        if json_target:
            raw_content = self.resolve_json(raw)
        else:
            form_target = eval(raw).get('form_data', [])
            raw_content = self.resolve_form_data(raw) if form_target else self.resolve_x_www_form_urlencoded(raw)
        return raw_content

    @staticmethod
    def resolve_script(
            use='setup_script',
            setup_script=None,
            teardown_script=None
    ):
        """
        {'script_code': "ep.get_env_variable('name')\nep.get_env_variable('name')\nep.get_env_variable('name')"}

        'setup_script': "print('前置脚本123')"
        """
        script = setup_script if use == 'setup_script' else teardown_script
        return script

    @staticmethod
    def resolve_extract(env="env", extract=None):
        """
        [{'id': 452947, 'edit': False, 'visible': False, 'name': 'router', 'type': 'jsonpath', 'value': '$.url'}]
        "extract": {
            # 通过jsonpath提取
            "router": ("env", "jsonpath", "$.url"),
            # 通过正则表达式提取
        }
        """
        extract_items = eval(extract)
        extract_data = {
            item['name']: (env, item['type'], item['value']) for item in extract_items
        }
        return extract_data

    @staticmethod
    def resolve_validators(validate=None):
        """
        [{'id': 713191, 'edit': False, 'visible': False, 'value': 'http://httpbin.org/post', 'type': '相等', 'name': '$.url'}]

        'validators': [{
            'method': '相等',
            'actual': 'http://httpbin.org/post',
            'expect': '$.url'}]
        }
        """
        validate_items = eval(validate)
        validate_data = [{
            'method': item['type'],
            'actual': item['value'],
            'expect': item['name']
        } for item in validate_items]
        return validate_data

    def get_api_template(self):
        """
        {
        "If": {"condition": 100 > 99},
        'Loop':2,
        "title": "测试用例2",
        "host": "http://httpbin.org/post",
        "interface": {
            "url": "http://httpbin.org/post",
            "name": "登录",
            "method": "post",
        },
        "headers": {
            'content-Type': "application/json"
        },
        "request": {
            'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
        },
        'setup_script': "print('前置脚本123')",
        'teardown_script': "test.assertion('相等',200,response.status_code)",
        "extract": {
            # 通过jsonpath提取
            "router": ("env", "jsonpath", "$.url"),
            # 通过正则表达式提取
        },
        'validators': [{
            'method': '相等',
            'actual': 'http://httpbin.org/post',
            'expect': '$.url'}]
        }
        """
        api_doc_template = {
            "mode": self.mode,
            "title": self.name,
            "interface": {
                "url": self.url,
                "name": self.name,
                "method": self.method
            },
            "threads": int(self.threads),
            "iterations": int(self.iterations),
            "headers": self.resolve_headers(self.headers),
            "request": self.raw_conversion(self.raw),
            'setup_script': self.resolve_script(setup_script=self.setup_script),
            'teardown_script': self.resolve_script(use='teardown_script', teardown_script=self.teardown_script),
            'extract': self.resolve_extract(extract=self.extract),
            'validators': self.resolve_validators(self.validate)
        }
        return api_doc_template

    def get_step_template(self, step):
        """
        "step_data": [
        {
            "name": "验证表单回填",
            "method": "POST",
            "url": "http://localhost:8080/login",
            "priority": 0,
            "status": 0,
            "desc": "http://localhost:8080/login",
            "headers": "[{\"name\": \"Content-Type\", \"value\": \"application/json\", \"description\": \"\"}, {\"name\": \"1\", \"value\": \"1\", \"description\": \"1\"}]",
            "params": "[{\"name\": \"dddd\", \"value\": \"4444\", \"description\": \"4444\", \"type\": \"Float\"}]",
            "raw": "{\"json\": \"{\\\"$schema\\\": \\\"http://json-schema.org/draft-04/schema\\\"}\"}",
            "setup_script": "ep.get_pre_url()",
            "teardown_script": "ep.get_pre_url()",
            "validate": "[{\"name\": \"1\", \"type\": \"\\u5927\\u4e8e\\u7b49\\u4e8e\", \"description\": \"3\"}]",
            "extract": "[{\"name\": \"1\", \"type\": \"jsonpath\", \"description\": \"1\"}]",
            "project": 158
        }
    ],
        """
        step_template = {
            "title": step.get('name', None),
            "interface": {
                "url": step.get('url', None),
                "name": step.get('name', None),
                "method": step.get('method', None)
            },
            "headers": self.resolve_headers(step.get('headers', [])),
            "request": self.raw_conversion(step.get('raw', {})),
            'setup_script': self.resolve_script(setup_script=step.get('setup_script', None)),
            'teardown_script': self.resolve_script(use='teardown_script',
                                                   teardown_script=step.get('teardown_script', None)),
            'extract': self.resolve_extract(extract=step.get('extract', [])),
            'validators': self.resolve_validators(step.get('validate', []))
        }
        return step_template

    def get_case_template(self, cases, name='Demo'):

        if not cases:
            return []  # or None

        return {
            'name': name,
            'cases': [self.get_step_template(step) for step in cases]
        }

    def get_plan_template(self, suites: List[dict]) -> List[dict]:

        if not suites:
            return []

        return [{
            'name': case.get('name', f'场景-{index + 1}'),
            'cases': [self.get_step_template(step) for step in case.get('cases', [])]
        } for index, case in enumerate(suites)]
