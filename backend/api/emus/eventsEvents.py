from api.emus.base import BaseEumWitchDesc


class EventTypeEum(BaseEumWitchDesc):

    AUTOTEST_EXECUTED = "自动化测试执行完成✅"
    AUTOTEST_CANCELLED = "自动化测试执行被取消❌"
    AUTOTEST_RETRY_EXCEPTION_CASE_STARTED = "自动开始重试异常用例✅"
    TEST_DATA_GENERATED = "测试数据已经生成✅"
