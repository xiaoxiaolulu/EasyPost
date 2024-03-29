from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from api.dao.https import HttpDao
from api.scheduler.base import BaseScheduler
from config.settings import TIME_ZONE
from utils.logger import logger as logging


class Trigger(CronTrigger):

    @classmethod
    def from_crontab(cls, expr, timezone=None):
        """
        Create a :class:`~CronTrigger` from a standard crontab expression.
        """
        values = expr.split()
        if len(values) < 0:
            raise ValueError('The parameter was incorrectly obtained, and the field number was 0')

        return cls(
            second=values[0],
            minute=values[1],
            hour=values[2],
            day=values[3],
            month=values[4],
            day_of_week=values[5],
            year=values[6],
            timezone=timezone
        )


class Scheduler(BaseScheduler):

    scheduler = BackgroundScheduler()

    @classmethod
    def configure(cls, **kwargs):
        cls.scheduler.configure(**kwargs)

    @classmethod
    def start(cls):
        cls.scheduler._logger = logging
        cls.scheduler.start()

    @classmethod
    def add_test_plan(cls, case_list, plan_id, plan_name, cron):

        return cls.scheduler.add_job(
            name=plan_name,
            func=HttpDao.run_test_suite,
            args=(case_list, plan_name, ),
            trigger=Trigger.from_crontab(cron),
            id=str(plan_id)
        )

    # @staticmethod
    # def edit_test_plan(plan_id, plan_name, cron):
    #     """
    #     通过测试计划id，更新测试计划任务的cron，name等数据
    #     :param plan_id:
    #     :param plan_name:
    #     :param cron:
    #     :return:
    #     """
    #     job = Scheduler.scheduler.get_job(str(plan_id))
    #     if job is None:
    #         # 新增job
    #         return Scheduler.add_test_plan(plan_id, plan_name, cron)
    #     Scheduler.scheduler.modify_job(job_id=str(plan_id), trigger=CronTrigger.from_crontab(cron), name=plan_name)
    #     Scheduler.scheduler.pause_job(str(plan_id))
    #     Scheduler.scheduler.resume_job(str(plan_id))

    @classmethod
    def pause_resume_test_plan(cls, plan_id, status):
        """
        暂停或恢复测试计划，会影响到next_run_at
        :param plan_id:
        :param status:
        :return:
        """
        if status:
            cls.scheduler.resume_job(job_id=str(plan_id))
        else:
            cls.scheduler.pause_job(job_id=str(plan_id))

    @classmethod
    def remove(cls, plan_id):
        """
        删除job，当删除测试计划时，调用此方法
        :param plan_id:
        :return:
        """
        cls.scheduler.remove_job(str(plan_id))

    # @staticmethod
    # def list_test_plan(data: List):
    #     ans = []
    #     for d, follow in data:
    #         temp = PityResponse.model_to_dict(d)
    #         temp['follow'] = follow is not None
    #         job = Scheduler.scheduler.get_job(str(temp.get('id')))
    #         if job is None:
    #             # 说明job初始化失败了
    #             temp["state"] = 2
    #             ans.append(temp)
    #             continue
    #         if job.next_run_time is None:
    #             # 说明job被暂停了
    #             temp["state"] = 3
    #         else:
    #             temp["next_run"] = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
    #         ans.append(temp)
    #     return ans
