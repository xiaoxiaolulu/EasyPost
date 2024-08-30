import copy
import time
import traceback
import unittest
from concurrent.futures.thread import ThreadPoolExecutor
from emus.CaseBaseEnum import (
    CaseStatusEnum,
    CaseStatusMessageEnum
)
from unitrunner.models.report import (
    TestCaseResult,
    TestReport
)


class TestResult(unittest.TestResult):

    def __init__(self):
        super().__init__()
        self.result: TestCaseResult = {
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
        Marks the beginning of a test execution, records the start time, and logs the test name.

        This method is typically used within a testing framework or class for managing test execution.

        Args:
            test: The test object that is about to start.
        """
        super().startTest(test)
        self.start_time = time.time() # noqa
        test.name = getattr(test, '_testMethodDoc')
        getattr(test, 'info_log')("开始执行用例：【{}】\n".format(test.name))

    def stopTest(self, test):
        """
        Marks the end of a test execution, calculates the run time, and updates test results.

        This method is typically used within a testing framework or class for managing test execution.

        Args:
            test: The test object that has just finished execution.
        """
        test.run_time = '{:.3}s'.format((time.time() - self.start_time))
        self.result['cases'].append(test)
        self.result['all'] += 1
        self.result["name"] = test.__class__.__name__

    def stopTestRun(self, title=None):
        """
        Marks the end of a test run, determines the overall test outcome, and updates the result dictionary.

        This method is typically used within a testing framework or class to finalize test execution and
        summarize the results.

        Args:
            title (str, optional): A title for the test run (defaults to None).
        """
        if len(self.errors) > 0:
            self.result['state'] = CaseStatusEnum.ERROR
        elif len(self.failures) > 0:
            self.result['state'] = CaseStatusEnum.FAIL
        else:
            self.result['state'] = CaseStatusEnum.SUCCESS

    def addSuccess(self, test):
        """
        Logs a successful test and updates the result dictionary.

        This method is typically called by a testing framework or class when a test completes successfully.

        Args:
            test: The test object that has just finished execution.
        """
        count = test._testMethodName.split("_").pop()
        self.result["success"] += 1
        test.state = CaseStatusMessageEnum.SUCCESS
        test.tag = f'循环{count}次' if count else '-'
        getattr(test, 'info_log')("{}执行——>【通过】\n".format(getattr(test, '_testMethodDoc')))

    def addFailure(self, test, err):
        """
        Logs a failed test, updates the result dictionary, and saves the error information.

        This method is typically called by a testing framework or class when a test fails.

        Args:
            test: The test object that has just finished execution.
            err: A tuple containing the error type and error message.
        """
        count = test._testMethodName.split("_").pop()
        super().addFailure(test, err)
        self.result["fail"] += 1
        test.state = CaseStatusMessageEnum.FAIL
        test.tag = f'循环{count}次' if count else '-'
        getattr(test, 'warning_log')(err[1])
        getattr(test, 'warning_log')("{}执行——>【失败】\n".format(getattr(test, '_testMethodDoc')))

    def addError(self, test, err):
        """
        Logs a test error, updates the result dictionary, and saves the error information.

        This method is typically called by a testing framework or class when a test encounters
        an error (unexpected exception).

        Args:
            test: The test object that has just finished execution.
            err: A tuple containing the error type, error message, and traceback information.
        """
        count = test._testMethodName.split("_").pop()
        super().addError(test, err)
        self.result["error"] += 1
        test.state = CaseStatusMessageEnum.ERROR
        test.tag = f'循环{count}次' if count else '-'
        getattr(test, 'error_log')(str(err[1]))
        getattr(test, 'error_log')("{}执行——>【错误Error】\n".format(getattr(test, '_testMethodDoc')))
        getattr(test, 'error_log')('\n'.join(traceback.format_exception(*err)))

    def addSkip(self, test, reason):
        """
        Logs a skipped test, updates the result dictionary, and saves the reason for skipping.

        This method is typically called by a testing framework or class when a test is skipped.

        Args:
            test: The test object that has just finished execution.
            reason: A string explaining why the test was skipped.
        """
        count = test._testMethodName.split("_").pop()
        super().addSkip(test, reason)
        test.state = CaseStatusMessageEnum.SKIP
        test.tag = f'循环{count}次' if count else '-'
        getattr(test, 'info_log')("{}执行--【跳过Skip】\n".format(getattr(test, '_testMethodDoc')))


class ReRunResult(TestResult):

    def __init__(self, count, interval):
        """
        Initializes a test runner object.

        This constructor is typically called when creating a new instance of the test runner class.

        Args:
            count (int): The total number of test cases to run.
            interval (float): The time interval (in seconds) between running each test case.
        """
        super().__init__()
        self.count = count
        self.interval = interval
        self.run_cases = []

    def startTest(self, test):
        """
        Called before each test case is run.

        This method is typically overridden by subclasses to perform any
        necessary setup before a test case is executed.

        Args:
            test: The test case that is about to be run.
        """
        if not hasattr(test, "count"):
            super().startTest(test)

    def stopTest(self, test):
        """
        Called after each test case is run.

        This method is typically overridden by subclasses to perform any necessary
        cleanup after a test case has been executed.

        Args:
            test: The test case that has just finished execution.
        """
        if test not in self.run_cases:
            self.run_cases.append(test)
            super().stopTest(test)

    def addFailure(self, test, err):
        """
        Logs a failed test, updates the result dictionary, and saves the error information.

        This method is typically called by a testing framework or class when a test fails.

        Args:
            test: The test object that has just finished execution.
            err: A tuple containing the error type and error message.
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
        Logs a test error, updates the result dictionary, and saves the error information.

        This method is typically called by a testing framework or class when a test
        encounters an error (unexpected exception).

        Args:
            test: The test object that has just finished execution.
            err: A tuple containing the error type, error message, and traceback information.
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            getattr(test, 'error_log')("{}执行——>【错误Error】\n".format(getattr(test, '_testMethodDoc')))
            getattr(test, 'exception_log')(err[1])
            getattr(test, 'error_log')("================{}重运行第{}次================\n".format(test, test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addError(test, err)
            if test.count != 0:
                getattr(test, 'info_log')("================重运行{}次完毕================\n".format(test.count))


class TestRunner:

    def __init__(self, suite, tester='测试员'):
        """
        Initializes a test runner object.

        This constructor is typically called when creating a new instance of the test runner class.

        Args:
            suite: The test suite to be run.
            tester: The name of the tester running the tests.
        """
        self.suite = suite
        self.tester = tester
        self.result_list = []
        self.starttime = time.time()

    def __classification_suite(self):
        """
        Classifies a test suite into smaller suites containing individual test cases.

        This method recursively traverses a test suite, identifying suites that directly
        contain test cases and isolating them for execution.

        Returns:
            list: A list of suites, each containing individual test cases.
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
        """
        Parses and aggregates test results into a comprehensive dictionary.

        This method iterates through the individual test results stored in
        `self.result_list` and builds a consolidated dictionary containing
        various test execution statistics.

        Returns:
            dict: A dictionary containing aggregated test results.
        """
        result: TestReport = {
            "class_list": [],
            "all": 0,
            "success": 0,
            "error": 0,
            "fail": 0,
            "runtime": "",
            "argtime": "",
            "begin_time": "",
            "pass_rate": 0,
            "state": ""
        }

        for cls in self.result_list:
            cases_info = cls.result['cases']
            result['all'] += cls.result['all']
            result['success'] += cls.result['success']
            result['error'] += cls.result['error']
            result['fail'] += cls.result['fail']

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
        result["state"] = "通过" if (result['success'] / result['all']) == 1.0 else "失败"
        return result

    def run(self, thread_count=1, rerun=0, interval=2):
        """
        Executes the test suite(s) using multithreading.

        This method orchestrates the test execution process. It performs the following steps:

        1. Classifies the test suite into smaller suites containing individual test cases.
        2. Creates a thread pool with the specified number of threads.
        3. Iterates through the classified suites:
           - Creates a `ReRunResult` object to store test results with retries.
           - Appends the `ReRunResult` object to `self.result_list` for tracking.
           - Submits the test suite's `run` method to the thread pool, providing the `ReRunResult` object as an argument
           - Attaches a callback function `res.stopTestRun` to be executed after the test suite finishes running.
        4. Waits for all threads to complete and parses the individual test results.
        5. Returns a dictionary containing aggregated test execution statistics.

        Args:
            thread_count (int, optional): The number of threads to use for parallel execution. Defaults to 1 (thread).
            rerun (int, optional): The maximum number of times to retry a failing test case. Defaults to 0 (no retries).
            interval (float, optional): The time interval (in seconds) to wait between retries. Defaults to 2.

        Returns:
            dict: A dictionary containing aggregated test results.
        """
        suites = self.__classification_suite()
        with ThreadPoolExecutor(max_workers=thread_count) as ts:
            for i in suites:
                res = ReRunResult(count=rerun, interval=interval)
                self.result_list.append(res)
                ts.submit(i.run, result=res).add_done_callback(res.stopTestRun)
        result = self.__parser_results()
        return result
