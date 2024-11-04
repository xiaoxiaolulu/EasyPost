from api.response.fatcory import ResponseStandard
from common.engine.base import run_test, run_api

if __name__ == '__main__':
    # 测试数据(详细结构说明看下一节)
    case_data = [
        # {
        #     'name': "测试场景名称1",
        #     'cases': [
        #         # {
        #         #     "title": "测试用例2",
        #         #     # 'Loop': 3,
        #         #     # 'children': [
        #         #     #     {
        #         #     #         "title": "测试用例2",
        #         #     #         'Loop': 2,
        #         #     #         'children': [{
        #         #     #             'Loop': 2,
        #         #     #             "title": "测试用例2",
        #         #     #             "host": "http://httpbin.org/post",
        #         #     #             "interface": {
        #         #     #                 "url": "http://httpbin.org/post",
        #         #     #                 "name": "登录",
        #         #     #                 "method": "post",
        #         #     #             },
        #         #     #             "headers": {
        #         #     #                 'content-Type': "application/json"
        #         #     #             },
        #         #     #             "request": {
        #         #     #                 'json': {"mobile_phone": "3333", "pwd": "lemonban"},
        #         #     #             },
        #         #     #             # 'setup_script': "print('前置脚本123')",
        #         #     #             # 'teardown_script': "test.assertion('相等',200,response.status_code)",
        #         #     #             "extract": {
        #         #     #                 # 通过jsonpath提取
        #         #     #                 "routers": ("env", "jsonpath", "$.url"),
        #         #     #                 # 通过正则表达式提取
        #         #     #             },
        #         #     #             'validators': [{
        #         #     #                 'method': '相等',
        #         #     #                 'actual': 'http://httpbin.org/post',
        #         #     #                 'expect': '$.url'}]
        #         #     #         }, ]
        #         #     #     }
        #         #     #
        #         #     #     # {
        #         #     #     #     "title": "xxx",
        #         #     #     #     'if': [{
        #         #     #     #         'method': '相等',
        #         #     #     #         'actual': 'http://httpbin.org/post',
        #         #     #     #         'expect': '$.user_mobile'}]
        #         #     #     # },
        #         #     #     # {
        #         #     #     #     "title": "测试用例44442",
        #         #     #     #     # "host": "http://httpbin.org/post",
        #         #     #     #     "interface": {
        #         #     #     #         "url": "http://httpbin.org/post",
        #         #     #     #         "name": "登录",
        #         #     #     #         "method": "post",
        #         #     #     #     },
        #         #     #     #     "headers": {
        #         #     #     #         'content-Type': "application/json"
        #         #     #     #     },
        #         #     #     #     "request": {
        #         #     #     #         'json': {"mobile_phone": "13564957378", "pwd": "lemonban"},
        #         #     #     #     },
        #         #     #     #     'setup_script': "print('前置脚本123')",
        #         #     #     #     'teardown_script': "ep.assertion('相等',200, 200)",
        #         #     #     #     # 'validators': [{
        #         #     #     #     #     'method': '相等',
        #         #     #     #     #     'actual': 'http://httpbin.org/post',
        #         #     #     #     #     'expect': '$.url'}]
        #         #     #     # },
        #         #     # ]
        #         #     # 'LOOP': {"condition": 100>99, "count": 12},
        #         #     # "host": "http://httpbin.org/post",
        #         #     # "interface": {
        #         #     #     "url": "http://httpbin.org/post",
        #         #     #     "name": "登录",
        #         #     #     "method": "post",
        #         #     # },
        #         #     # "headers": {
        #         #     #     'content-Type': "application/json"
        #         #     # },
        #         #     # "request": {
        #         #     #     'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
        #         #     # },
        #         #     # 'setup_script': "print('前置脚本123')",
        #         #     # #'teardown_script': "test.assertion('相等',200,response.status_code)",
        #         #     #  #   "extract": {
        #         #     #  #       # 通过jsonpath提取
        #         #     #  #       "routers": ("env", "jsonpath", "$.url"),
        #         #     #         # 通过正则表达式提取
        #         #     #  #   },
        #         #     # 'validators': [{
        #         #     #     'method': '相等',
        #         #     #     'actual': 'http://httpbin.org/post',
        #         #     #     'expect': '$.url'}]
        #         # },
        #         # {
        #         #     "title": "xxx",
        #         #     'if': [{
        #         #         'method': '相等',
        #         #         'actual': 'http://httpbin.org/post',
        #         #         'expect': '$.user_mobile'}]
        #         # },
        #         {
        #             "title": "33333333",
        #             # "host": "http://httpbin.org/post",
        #             "interface": {
        #                 "url": "http://httpbin.org/post",
        #                 "name": "登录",
        #                 "method": "post",
        #             },
        #             "headers": {
        #                 'content-Type': "application/json"
        #             },
        #             "request": {
        #                 'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
        #             },
        #             'setup_script': "global_func.get_timestamp()",
        #             'teardown_script': "ep.assertion('相等',200, 200)",
        #             'validators': [{
        #                 'method': '相等',
        #                 'actual': 'http://httpbin.org/post',
        #                 'expect': '$.url'}],
        #             "extract": {
        #                 # 通过jsonpath提取
        #                 "routers": ("env", "jsonpath", "$.url"),
        #                 # 通过正则表达式提取
        #             }
        #         },
        #     ]
        # },
        {
            'name': "测试场景名称1",
            'cases': [
                # {
                #     "title": "测试用例2",
                #     # 'Loop': 3,
                #     # 'children': [
                #     #     {
                #     #         "title": "测试用例2",
                #     #         'Loop': 2,
                #     #         'children': [{
                #     #             'Loop': 2,
                #     #             "title": "测试用例2",
                #     #             "host": "http://httpbin.org/post",
                #     #             "interface": {
                #     #                 "url": "http://httpbin.org/post",
                #     #                 "name": "登录",
                #     #                 "method": "post",
                #     #             },
                #     #             "headers": {
                #     #                 'content-Type': "application/json"
                #     #             },
                #     #             "request": {
                #     #                 'json': {"mobile_phone": "3333", "pwd": "lemonban"},
                #     #             },
                #     #             # 'setup_script': "print('前置脚本123')",
                #     #             # 'teardown_script': "test.assertion('相等',200,response.status_code)",
                #     #             "extract": {
                #     #                 # 通过jsonpath提取
                #     #                 "routers": ("env", "jsonpath", "$.url"),
                #     #                 # 通过正则表达式提取
                #     #             },
                #     #             'validators': [{
                #     #                 'method': '相等',
                #     #                 'actual': 'http://httpbin.org/post',
                #     #                 'expect': '$.url'}]
                #     #         }, ]
                #     #     }
                #     #
                #     #     # {
                #     #     #     "title": "xxx",
                #     #     #     'if': [{
                #     #     #         'method': '相等',
                #     #     #         'actual': 'http://httpbin.org/post',
                #     #     #         'expect': '$.user_mobile'}]
                #     #     # },
                #     #     # {
                #     #     #     "title": "测试用例44442",
                #     #     #     # "host": "http://httpbin.org/post",
                #     #     #     "interface": {
                #     #     #         "url": "http://httpbin.org/post",
                #     #     #         "name": "登录",
                #     #     #         "method": "post",
                #     #     #     },
                #     #     #     "headers": {
                #     #     #         'content-Type': "application/json"
                #     #     #     },
                #     #     #     "request": {
                #     #     #         'json': {"mobile_phone": "13564957378", "pwd": "lemonban"},
                #     #     #     },
                #     #     #     'setup_script': "print('前置脚本123')",
                #     #     #     'teardown_script': "ep.assertion('相等',200, 200)",
                #     #     #     # 'validators': [{
                #     #     #     #     'method': '相等',
                #     #     #     #     'actual': 'http://httpbin.org/post',
                #     #     #     #     'expect': '$.url'}]
                #     #     # },
                #     # ]
                #     # 'LOOP': {"condition": 100>99, "count": 12},
                #     # "host": "http://httpbin.org/post",
                #     # "interface": {
                #     #     "url": "http://httpbin.org/post",
                #     #     "name": "登录",
                #     #     "method": "post",
                #     # },
                #     # "headers": {
                #     #     'content-Type': "application/json"
                #     # },
                #     # "request": {
                #     #     'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
                #     # },
                #     # 'setup_script': "print('前置脚本123')",
                #     # #'teardown_script': "test.assertion('相等',200,response.status_code)",
                #     #  #   "extract": {
                #     #  #       # 通过jsonpath提取
                #     #  #       "routers": ("env", "jsonpath", "$.url"),
                #     #         # 通过正则表达式提取
                #     #  #   },
                #     # 'validators': [{
                #     #     'method': '相等',
                #     #     'actual': 'http://httpbin.org/post',
                #     #     'expect': '$.url'}]
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
                    # "host": "http://httpbin.org/post",
                    "interface": {
                        "url": "/post",
                        "name": "登录",
                        "method": "post",
                    },
                    "headers": {
                        'content-Type': "application/json"
                    },
                    "request": {
                        'json': {"mobile_phone": "31313131313131", "pwd": "lemonban"},
                    },
                    # 'setup_script': "print('前置脚本123')",
                    # 'teardown_script': "ep.assertion('相等',200, 200)",
                    # 'validators': [{
                    #     'method': '相等',
                    #     'actual': 'http://httpbin.org/post',
                    #     'expect': '$.url'}],
                    # "extract": {
                    #     # 通过jsonpath提取
                    #     "routers": ("env", "jsonpath", "$.url"),
                    #     # 通过正则表达式提取
                    # }
                },
            ]
        }
    ]
    #    运行环境数据(详细结构说明看第三节)
    config = {
        'ENV': {
            "host": 'http://httpbin.org',
            'user_mobile': 999999999},
        'db': [{}, {}],
        'global_func': "print('前置脚本123')",
        'rerun': 1
    }
    # api_data =  {
    #     #"If": {"condition": 100 > 99},
    #     #'Loop':2,
    #     # "mode": "perform",
    #     "title": "测试用例2",
    #     "threads": 1,
    #     "iterations": 1,
    #     "host": "http://httpbin.org/post",
    #     "interface": {
    #         "url": "http://httpbin.org/post",
    #         "name": "登录",
    #         "method": "post",
    #     },
    #     "headers": {
    #         'content-Type': "application/json"
    #     },
    #     "request": {
    #         'json': {"mobile_phone": "13564957378", "pwd": "lemonban"},
    #     },
    #     #'setup_script': "print('前置脚本123')",
    #     #'teardown_script': "test.assertion('相等',200,response.status_code)",
    #         "extract": {
    #             # 通过jsonpath提取
    #             "routers": ("env", "jsonpath", "$.url"),
    #             # 通过正则表达式提取
    #         },
    #     'validators': [{
    #         'method': '相等',
    #         'actual': 'http://httpbin.org/post',
    #         'expect': '$.url'}]
    # }
    # result = run_test(env_config=config, case_data=case_data, debug=False)
    result = run_api(api_data={'mode': 'normal', 'title': '33333', 'interface': {'url': 'http://httpbin.org/post', 'name': '33333', 'method': 'POST'}, 'headers': {}, 'request': {'data': {}}, 'setup_script': '', 'teardown_script': '', 'extract': {}, 'validators': []})
    import json

    r = json.dumps(ResponseStandard.encode_json(result), ensure_ascii=False)
    print(r)
    # result = run_api(api_data)
    #
    #
    # r = json.dumps(ResponseStandard.encode_json(result), ensure_ascii=False)
    # print(r)
