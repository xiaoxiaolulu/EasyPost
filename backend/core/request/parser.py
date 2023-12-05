class HandelTestData(object):

    def __init__(self, request_body=None):
        try:
            # 额外参数
            self.directory_id = request_body.get('directory_id', None)
            self.project = request_body.get('project', None)

            # 基本信息
            self.name = request_body.get('name', None)
            self.url = request_body.get('url', None)
            self.method = request_body.get('method', None)
            self.tags = request_body.get('tags', None)
            self.status = request_body.get('status', None)
            self.desc = request_body.get('desc', None)

            # 请求体
            self.headers = request_body.get('headers', {})
            self.raw = request_body.get('raw', {})
            self.params = request_body.get('params', None)
            self.setup_script = request_body.get('setup_script', None)
            self.teardown_script = request_body.get('teardown_script', None)
            self.validate = request_body.get('validate', [])
            self.extract = request_body.get('extract', {})
        except (KeyError, ValueError, AttributeError):
            pass

    def resolve_headers(self):
        """
        [{'name': 'Content-Type', 'value': 'application/json', 'description': '', 'edit': False}]

        "headers": {
            'content-Type': "application/json"
        },
        """
        headers = {item['name']: item['value'] for item in self.headers}
        return headers

    def resolve_form_data(self):
        """
        {'data': [{'id': 912586, 'edit': False, 'visible': False, 'name': '33', 'value': '333', 'type': 'Integer', 'description': '33'}]}

        'data': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
        """
        form_data_items = self.raw.get('data', [])
        form_data = {
            'data': {item['name']: item['value'] for item in form_data_items}
        }
        return form_data

    def resolve_json(self):
        """
        {'json': '{"$schema": "http://json-schema.org/draft-04/schema"}'}
        """
        json_items = self.raw.get('json', [])
        json_data = {
            'json': json_items
        }
        return json_data

    def raw_conversion(self):
        target = self.raw.get('data', [])
        raw_content = self.resolve_form_data() if target else self.resolve_json()
        return raw_content

    def resolve_script(self, use='setup_script'):
        """
        {'script_code': "ep.get_env_variable('name')\nep.get_env_variable('name')\nep.get_env_variable('name')"}

        'setup_script': "print('前置脚本123')"
        """
        script = self.setup_script if use == 'setup_script' else self.teardown_script
        script = script.get('script_code', None)
        return script

    def resolve_extract(self, env="env"):
        """
        [{'id': 452947, 'edit': False, 'visible': False, 'name': 'router', 'type': 'jsonpath', 'value': '$.url'}]
        "extract": {
            # 通过jsonpath提取
            "router": ("env", "jsonpath", "$.url"),
            # 通过正则表达式提取
        }
        """
        extract_items = self.extract
        extract_data = {
            item['name']: (env, item['type'], item['value']) for item in extract_items
        }
        return extract_data

    def resolve_validators(self):
        """
        [{'id': 713191, 'edit': False, 'visible': False, 'value': 'http://httpbin.org/post', 'type': '相等', 'name': '$.url'}]

        'validators': [{
            'method': '相等',
            'actual': 'http://httpbin.org/post',
            'expect': '$.url'}]
        }
        """
        validate_items = self.validate
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
            "title": self.name,
            "interface": {
                "url": self.url,
                "name": self.name,
                "method": self.method
            },
            "headers": self.resolve_headers(),
            "request": self.raw_conversion(),
            'setup_script': self.resolve_script(),
            'teardown_script':  self.resolve_script('teardown_script'),
            'extract': self.resolve_extract(),
            'validators': self.resolve_validators()
        }
        return api_doc_template
