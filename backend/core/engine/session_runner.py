import importlib
import os
from typing import Any
from core.engine.env import db  # noqa
from core.engine.generate import GenerateCase
from core.engine.runner import TestRunner
from utils.logger import logger

try:
    global_func = importlib.import_module('global_func')
except ModuleNotFoundError:
    from core.builitin import functions as global_func


def run_test(case_data, env_config={}, tester='测试员', thread_count=1, debug=True) -> tuple[Any, dict[Any, Any]] | Any: # noqa
    """
    :param case_data: 测试套件数据
    :param env_config: 用例执行的环境配置
        env_config:{
        'ENV':{"host":'http//:127.0.0.1'},
        'db':[{},{}],
        'FuncTools':'工具函数文件'
        }
    :param thread_count: 运行线程数
    :param debug: 单接口调试用debug模式
    :param tester: 测试员
    :return:
        debug模式：会返回本次运行的结果和 本次运行设置的全局变量，
    """
    global global_func, db, DEBUG, ENV, result # noqa
    global_func_file = env_config.get('global_func', b'')
    if global_func_file:
        with open('global_func.py', 'w', encoding='utf-8') as f:
            f.write(global_func_file)  # noqa

    # 更新运行环境
    global_func = importlib.reload(global_func)
    DEBUG = debug
    ENV = {**env_config.get('ENV', {})}
    db.init_connect(env_config.get('db', []))
    # 失败重跑
    rerun = env_config.get('rerun', 0)
    # 生成测试用例
    suite = GenerateCase().data_to_suite(case_data)
    # 运行测试用例
    runner = TestRunner(suite=suite, tester=tester)
    result = runner.run(thread_count=thread_count, rerun=rerun)
    if global_func and global_func_file:
        os.remove('global_func.py')
    # 断开数据库连接
    db.close_connect()
    if debug:
        return result, ENV
    else:
        return result



def run_api(api_data, tester='测试员', thread_count=1) -> tuple[Any, dict[Any, Any]] | Any: # noqa
    global result # noqa
    # 生成测试用例
    logger.debug("测试")
    suite = GenerateCase().data_to_suite(api_data)
    logger.debug(str(suite))
    # 运行测试用例
    runner = TestRunner(suite=suite, tester=tester)
    result = runner.run(thread_count=thread_count)
    # 断开数据库连接
    db.close_connect()
    return result
