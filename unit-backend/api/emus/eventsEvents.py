from enum import Enum


class EventTypeEum(Enum):

    SCHEDULED_START = 1, "调度程序启动✅"
    SCHEDULED_SHUTDOWN = 2, "调度程序关闭❌"
    SCHEDULED_PAUSE = 4, "调度程序中任务处理暂停⏯️"
    SCHEDULED_RENEW = 8, "调度程序中任务处理恢复✅"
    SCHEDULED_ADD = 16, "将执行器添加到调度程序中✅"
    SCHEDULED_DEL = 32, "执行器从调度程序中删除❌"
    SCHEDULED_STORE_ADD = 64, "将任务存储添加到调度程序中✅"
    SCHEDULED_STORE_DEL = 128, "任务存储从调度程序中删除✅"
    SCHEDULED_TASK_STORE_DEL = 256, "所有任务从所有任务存储中删除或从一个特定的任务存储中删除❌"
    SCHEDULED_ADD_NEW_TASK = 512, "添加新的定时任务✅"
    SCHEDULED_STORE_DEL_TASK = 1024, "从任务存储中删除了任务❌"
    SCHEDULED_UPDATE_TASK = 2048, "从调度程序外部修改了任务✅"
    SCHEDULED_EXECUTE_SUCCESS = 4096, "任务执行成功✅"
    SCHEDULED_EXECUTE_ERROR = 8192, "任务在执行期间引发异常⚠️"
    SCHEDULED_EXECUTE_WRONG = 16384, "错误了任务执行🚫"
    SCHEDULED_EXECUTED = 32768, "任务已经提交到执行器中执行✅"
    SCHEDULED_EXECUTE_MAXIMUM = 65536, "任务因为达到最大并发执行时，触发的事件⬆️"

    def __new__(cls, value, msg):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.msg = msg
        return obj

    def __str__(self):
        return f"{self.name}: {self.msg}"
