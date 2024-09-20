import json
import sys
from unitrunner.engine.base import run_test, run_api
from utils.logger import logger

if __name__ == '__main__':
    # "loop/for/while/http/if"
    case_data = [{
        'name': "测试场景名称1",
        'cases': [{
            "title": "测试用例2",
            "host": "http://httpbin.org/post",
            "interface": {
                "url": "/post",
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
            'teardown_script': "test.assertion('相等',200,response.status_code)"
        }]
    }]
    config = {
        'ENV': {
            "host": 'http://httpbin.org',
            'user_mobile': 999999999},
        'db': [{}, {}],
        'global_func': "print('前置脚本123')",
        'rerun': 1
    }
    # response = run_test(env_config=config, case_data=case_data, debug=False)
    # sys.stdout.write("测试结果\n")
    # sys.stdout.write(str(response))
    # sys.stdout.write("\n测试结果\n")
    api_doc = api_data = {
            "title": "demo",
            "interface": {
                "url": "https://www.baidu.com/",
                "name": "33333",
                "method": "GET"
            },
            "headers": {},
            "request": {"data": {}},
            "setup_script": "",
            "teardown_script": "",
            "extract": {},
            "validators": []
        }
    responses = run_api(api_data=api_doc)
    print(responses)
    print(json.dumps(dict(responses), ensure_ascii=False, indent=2))
