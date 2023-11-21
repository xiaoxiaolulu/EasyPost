from api.response.fatcory import ResponseStandard
from core.request.cases import run_test

if __name__ == '__main__':
    # 测试数据(详细结构说明看下一节)
    case_data = [{
        'name': "测试场景名称1",
        'cases': [
            # {
            # "title": "测试用例2",
            # # "IF": {"condition": 100>99},
            # # 'LOOP': {"condition": 100>99, "count": 12},
            # "host": "http://httpbin.org/post",
            # "interface": {
            #     "url": "/post",
            #     "name": "登录",
            #     "method": "post",
            # },
            # "headers": {
            #     'content-Type': "application/json"
            # },
            # "request": {
            #     'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
            # },
            # 'setup_script': "print('前置脚本123')",
            # # 'teardown_script': "test.assertion('相等',200,response.status_code)",
            # #     "extract": {
            # #         # 通过jsonpath提取
            # #         "router": ("env", "jsonpath", "$.url"),
            # #         # 通过正则表达式提取
            # #     },
            # 'validators': [{
            #     'method': '相等',
            #     'actual': 'http://httpbin.org/post',
            #     'expect': '$.url'}]
            # },
            # {
            #     "title": "xxx",
            #     'if': [{
            #         'method': '相等',
            #         'actual': 'http://httpbin.org/post',
            #         'expect': '$.user_mobile'}]
            # },
            {
                "title": "测试用例44442",
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
                    'json': {"mobile_phone": "13564957378", "pwd": "lemonban"},
                },
                'setup_script': "print('前置脚本123')",
                'teardown_script': "ep.assertion('相等',200, 200)",
                # 'validators': [{
                #     'method': '相等',
                #     'actual': 'http://httpbin.org/post',
                #     'expect': '$.url'}]
            },
        ]
    }]
    # 运行环境数据(详细结构说明看第三节)
    config = {
        'ENV': {"host": 'http://httpbin.org/post', 'user_mobile': 13564957378},
        'db': [{}, {}],
        'global_func': "print('前置脚本123')",
        'rerun': 1
    }
    result = run_test(
        case_data=case_data,
        env_config=config,
        debug=False
    )
    import json

    r = json.dumps(ResponseStandard.encode_json(result), ensure_ascii=False)
    print(r)
