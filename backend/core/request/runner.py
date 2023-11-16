import copy
import time
import traceback
import unittest
from concurrent.futures.thread import ThreadPoolExecutor


class TestResult(unittest.TestResult):
    """ 测试结果记录"""

    def __init__(self):
        super().__init__()

        self.result = {
            "all": 0,
            "success": 0,
            "fail": 0,
            "error": 0,
            "cases": [],
            "res": "",
            "name": ""
        }

    def startTest(self, test):
        """
        当测试用例测试即将运行时调用
        :return:
        """
        super().startTest(test)
        self.start_time = time.time() # noqa
        test.name = getattr(test, '_testMethodDoc')
        getattr(test, 'info_log')("开始执行用例：【{}】\n".format(test.name))

    def stopTest(self, test):
        """
        当测试用列执行完成后进行调用
        :return:
        """
        test.run_time = '{:.3}s'.format((time.time() - self.start_time))
        self.result['cases'].append(test)
        self.result['all'] += 1
        self.result["name"] = test.__class__.__name__

    def stopTestRun(self, title=None):
        """
        测试用例执行完手动调用统计测试结果的相关数据
        :param title:
        :return:
        """
        if len(self.errors) > 0:
            self.result['state'] = 'error'
        elif len(self.failures) > 0:
            self.result['state'] = 'fail'
        else:
            self.result['state'] = 'success'

    def addSuccess(self, test):
        """用例执行通过，成功数量+1"""
        self.result["success"] += 1
        test.state = '成功'
        getattr(test, 'info_log')("{}执行——>【通过】\n".format(getattr(test, '_testMethodDoc')))

    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        super().addFailure(test, err)
        self.result["fail"] += 1
        test.state = '失败'
        # 保存错误信息
        getattr(test, 'warning_log')(err[1])
        getattr(test, 'warning_log')("{}执行——>【失败】\n".format(getattr(test, '_testMethodDoc')))

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        super().addError(test, err)
        self.result["error"] += 1
        test.state = '错误'
        getattr(test, 'error_log')(str(err[1]))
        getattr(test, 'error_log')("{}执行——>【错误Error】\n".format(getattr(test, '_testMethodDoc')))
        getattr(test, 'error_log')(''.join(traceback.format_exception(*err)))

    def addSkip(self, test, reason):
        """
        修改跳过用例的状态
        :param test:测试用例
        :param reason: 相关信息
        :return: None
        """
        super().addSkip(test, reason)
        test.state = '跳过'
        getattr(test, 'info_log')("{}执行--【跳过Skip】\n".format(getattr(test, '_testMethodDoc')))


class ReRunResult(TestResult):

    def __init__(self, count, interval):
        super().__init__()
        self.count = count
        self.interval = interval
        self.run_cases = []

    def startTest(self, test):
        if not hasattr(test, "count"):
            super().startTest(test)

    def stopTest(self, test):
        if test not in self.run_cases:
            self.run_cases.append(test)
            super().stopTest(test)

    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            getattr(test, 'warning_log')("{}执行——>【失败Failure】\n".format(test))
            for string in traceback.format_exception(*err):
                getattr(test, 'warning_log')(string)
            getattr(test, 'warning_log')("开始第{}次重运行\n".format(test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addFailure(test, err)
            if test.count != 0:
                getattr(test, 'warning_log')("重运行{}次完毕\n".format(test.count))

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            getattr(test, 'error_log')("{}执行——>【错误Error】\n".format(test))
            getattr(test, 'exception_log')(err[1])
            getattr(test, 'error_log')("================{}重运行第{}次================\n".format(test, test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addError(test, err)
            if test.count != 0:
                getattr(test, 'info_log')("================重运行{}次完毕================\n".format(test.count))


class TestRunner:
    """测试运行器"""

    def __init__(self, suite, tester='测试员'):
        """套件"""
        self.suite = suite
        self.tester = tester
        self.result_list = []
        self.starttime = time.time()

    def __classification_suite(self):
        """
        将测试套件中的用例，根据用例类位单位，拆分成多个测试套件，打包成列表类型
        :return: list-->[suite,suite,suite.....]
        """
        suites_list = []

        def wrapper(suite):
            for item in suite:
                if isinstance(item, unittest.TestCase):
                    suites_list.append(suite)
                    break
                else:
                    wrapper(item)

        wrapper(copy.deepcopy(self.suite))
        return suites_list

    def __parser_results(self):
        """解析汇总测试结果"""
        result = {
            "class_list": [],
            "all": 0,
            "success": 0,
            "error": 0,
            "fail": 0,
            "runtime": "",
            "argtime": "",
            "begin_time": "",
            "pass_rate": 0
        }
        for cls in self.result_list:
            cases_info = cls.result['cases']
            result['all'] += cls.result['all']
            result['success'] += cls.result['success']
            result['error'] += cls.result['error']
            result['fail'] += cls.result['fail']
            # 将对象转换为dict类型数据
            cls.result['cases'] = [{k: v for k, v in res.__dict__.items() if not k.startswith('_')} for res in
                                   cases_info]
            result['class_list'].append(cls.result)
        result['runtime'] = '{:.2f}s'.format(time.time() - self.starttime)
        result['argtime'] = '{:.2f}s'.format(round((time.time() - self.starttime)/result.get('all', 0), 2))
        result["begin_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.starttime))
        result["tester"] = self.tester
        if result['all'] != 0:
            result['pass_rate'] = "{:.2f}%".format(result['success'] / result['all'] * 100) # noqa
        else:
            result['pass_rate'] = 0
        return result

    def run(self, thread_count=1, rerun=0, interval=2):
        """
        支持多线程执行
        注意点：如果多个测试类共用某一个全局变量，由于资源竞争可能会出现错误
        :param thread_count:线程数量，默认位1
        :param rerun:
        :param interval:
        :return:测试运行结果
        """
        # 将测试套件按照用例类进行拆分
        suites = self.__classification_suite()
        with ThreadPoolExecutor(max_workers=thread_count) as ts:
            for i in suites:
                res = ReRunResult(count=rerun, interval=interval)
                self.result_list.append(res)
                ts.submit(i.run, result=res).add_done_callback(res.stopTestRun)
        result = self.__parser_results()
        return result
