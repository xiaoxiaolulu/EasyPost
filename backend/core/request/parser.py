

class HandelTestData(object):

    def __init__(self, request_body):
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
            self.setup_script = request_body.get('setup_script', None)
            self.teardown_script = request_body.get('teardown_script', None)
            self.validate = request_body.get('validate', [])
            self.extract = request_body.get('extract', {})
        except (KeyError, ValueError, AttributeError):
            pass

    def handle_api_doc(self):
        return {
            "title": self.name,
            "interface": {
                "url": self.url,
                "name": self.name,
                "method": self.method,
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
