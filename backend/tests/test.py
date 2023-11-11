from core.request.cases import run_test


if __name__ == '__main__':
    # 测试数据(详细结构说明看下一节)
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
        },{
            "title": "测试用例3",
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
    # 运行环境数据(详细结构说明看第三节)
    config = {
        'ENV': {"host": 'http://httpbin.org/post', 'user_mobile': 13564957378},
        'db': [{}, {}],
        'global_func': "print('前置脚本123')"
    }
    result, a = run_test(
        case_data=case_data,
        env_config=config,
        )
    import json
    print(json.dumps(result))

