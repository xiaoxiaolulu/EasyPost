from datetime import datetime
from apscheduler.events import JobExecutionEvent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from api.dao.https import HttpDao
from api.emus.eventsEvents import EventTypeEum
from api.scheduler.base import BaseScheduler
from api.scheduler.config import config
from utils.logger import logger as logging


class Trigger(CronTrigger):

    @classmethod
    def from_crontab(cls, expr, timezone=None):
        """
        Creates an instance of the class (likely a cron-related class) from a crontab expression.

        Args:
            cls: The class to instantiate (assumed to handle cron scheduling).
            expr: The crontab expression string (e.g., "0 0 * * *").
            timezone: The optional timezone for the cron schedule (defaults to None).

        Returns:
            An instance of the class with fields set according to the crontab expression.

        Raises:
            ValueError: If the crontab expression is invalid (has 0 or fewer fields).
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
    def configure(cls):
        """
        Configures the scheduler (likely used for scheduling jobs) with the provided keyword arguments.

        This class method allows for centralized configuration of the scheduler used by the class.

        Args:
            **kwargs: Keyword arguments to pass to the scheduler's `configure` method.

        Returns:
            None: The method does not return any value.
        """
        cls.scheduler.configure(config)

    @classmethod
    def start(cls):
        """
        Starts the scheduler (likely used for scheduling jobs).

        This method starts the scheduler used by the class, which can
        be used to schedule jobs based on cron expressions.

        Returns:
            None: The method does not return any value.
        """
        cls.configure()
        cls.scheduler._logger = logging
        cls.scheduler.start()
        cls.scheduler.add_listener(cls._listener)
        cls.test_task()

    @staticmethod
    @scheduler.scheduled_job(trigger="interval", seconds=1)
    def test_task():
        raise "This is my task"

    @classmethod
    def _listener(cls, event: JobExecutionEvent):
        """
        This function is a listener that reacts to job execution events.

        Args:
            cls (class): The class instance where the listener is attached (usually the scheduler itself).
            event (JobExecutionEvent): The event object containing details about the job execution.
        """

        code = event.code
        run_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        jobstore = cls.scheduler._jobstores['default']
        job_history_data = dict()

        if code == EventTypeEum.SCHEDULED_EXECUTE_SUCCESS.value:
            job_id = event.job_id
            job_history_data['job_id'] = job_id
            job_history_data['run_time'] = run_time
            job_history_data['status'] = "SUCCESS"
            jobstore.insert_job_history(job_history_data)
        if code in [EventTypeEum.SCHEDULED_EXECUTE_ERROR.value, EventTypeEum.SCHEDULED_EXECUTE_WRONG.value]:
            job_id = event.job_id
            job_history_data['job_id'] = job_id
            job_history_data['run_time'] = run_time
            job_history_data['is_error'] = 1
            job_history_data['status'] = "FAILURE"
            job_history_data['error_msg'] = EventTypeEum.SCHEDULED_EXECUTE_ERROR.msg
            jobstore.insert_job_history(job_history_data)

    @classmethod
    def add_test_plan(cls, case_list, plan_id, plan_name, cron):
        """
        Schedules a test plan using the scheduler.

        This class method adds a new test plan to the scheduler using the provided details.

        Args:
            cls: The class itself.
            case_list: A list of test cases to be included in the plan.
            plan_id: The unique identifier of the test plan.
            plan_name: The human-readable name of the test plan.
            cron: The cron expression defining the schedule for running the test plan.

        Returns:
            Job: The scheduled job object representing the test plan.
        """
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
        Pauses or resumes a scheduled test plan based on the provided status.

        This class method allows for controlling the execution of a test plan.

        Args:
            cls: The class itself.
            plan_id: The unique identifier of the test plan.
            status: Boolean value indicating the desired action:
                - True: Resume the paused test plan.
                - False: Pause the running test plan.
        """
        if status:
            cls.scheduler.resume_job(job_id=str(plan_id))
        else:
            cls.scheduler.pause_job(job_id=str(plan_id))

    @classmethod
    def remove(cls, plan_id):
        """
        Removes a test plan from the scheduler.

        This class method removes a scheduled test plan based on its unique identifier.

        Args:
            cls: The class itself.
            plan_id: The unique identifier of the test plan to be removed.
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
