# import json
# import sys
# from unitrunner.engine.base import run_test, run_api
# from utils.logger import logger
#
# if __name__ == '__main__':
#     # "loop/for/while/http/if"
#     case_data = [{
#         'name': "测试场景名称1",
#         'cases': [{
#             "title": "测试用例2",
#             "host": "http://httpbin.org/post",
#             "interface": {
#                 "url": "/post",
#                 "name": "登录",
#                 "method": "post",
#             },
#             "headers": {
#                 'content-Type': "application/json"
#             },
#             "request": {
#                 'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
#             },
#             'setup_script': "print('前置脚本123')",
#             'teardown_script': "test.assertion('相等',200,response.status_code)"
#         }]
#     }]
#     config = {
#         'ENV': {
#             "host": 'http://httpbin.org',
#             'user_mobile': 999999999},
#         'db': [{}, {}],
#         'global_func': "print('前置脚本123')",
#         'rerun': 1
#     }
#     # response = run_test(env_config=config, case_data=case_data, debug=False)
#     # sys.stdout.write("测试结果\n")
#     # sys.stdout.write(str(response))
#     # sys.stdout.write("\n测试结果\n")
#     api_doc = api_data = {
#         "type": "loop",
#         "parameters": {
#             "count": 2
#         },
#         "children": [{
#             "type": "http",
#             "title": "demo",
#             "interface": {
#                 "url": "http://httpbin.org/post",
#                 "name": "33333",
#                 "method": "POST"
#             },
#             "headers": {},
#             "request": {"data": {}},
#             "setup_script": "",
#             "teardown_script": "",
#             "extract": {},
#             "validators": []
#         }]
#     }
#     responses = run_api(api_data=api_doc)
#     sys.stdout.write(str(responses))
#     logger.info(
#         f"--------  测试结果 ----------\n"
#         f"{json.dumps(responses, indent=4, ensure_ascii=False)}\n"
#     )

import random
import re
import socket
import struct
from dns import resolver

# 配置自定义 DNS 服务器
custom_resolver = resolver.Resolver()
custom_resolver.nameservers = ['127.0.0.1']
# 设置端口号（这里假设所有服务器都使用 8600 端口）
custom_resolver.port = 8600  # 注意：通常不需要对每个服务器单独设置，除非它们使用不同端口


def extract_ip_prefix(encoded_address: str):
    match = encoded_address.split(".")[0]
    return match


def decode_address(encoded_address):
    hex_address = extract_ip_prefix(encoded_address)
    binary_address = bytes.fromhex(hex_address)
    return socket.inet_ntoa(binary_address)


def srv_to_address_random_choice(srv_record_name):
    try:
        answer = custom_resolver.resolve(srv_record_name, 'SRV')
        selected_rdata = random.choice(answer)
        ip_address = decode_address(selected_rdata.target.to_text())
        print(f"Service: {srv_record_name} - {ip_address}:{selected_rdata.port} ")
        return ip_address, selected_rdata.port
    except resolver.NoAnswer as e:
        print(f"No answer found for the query: {srv_record_name}")
    except resolver.NXDOMAIN as e:
        print(f"Domain not found: {srv_record_name}")
    except Exception as e:
        print(f"Error occurred while resolving DNS: {str(e)}")


def main():
    # 查询 SRV 记录
    srv_record_name = 'unit_executor.service.consul'
    # srv_record_name = 'consul.service.consul'
    srv_to_address_random_choice(srv_record_name)


if __name__ == "__main__":
    main()
