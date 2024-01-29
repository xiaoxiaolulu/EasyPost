from typing import Any
from channels.db import database_sync_to_async
from django.forms import model_to_dict
from api.dao.https import HttpDao
from api.models.plan import Plan
from api.models.project import Project
from api.response.fatcory import ResponseStandard
from api.scheduler.scheduler import Scheduler
from core.request.parser import HandelTestData


class PlanDao:

    @staticmethod
    def parser_plan_data(request: Any, pk=None):
        api = HandelTestData(request.data)

        if pk:
            update_obj = Plan.objects.get(id=pk)
            project = update_obj.project
        else:
            project = Project.objects.get(id=api.project)

        request_body = {
            'name': api.name,
            'project': project,
            'cron': api.cron,
            'priority': api.priority,
            'state': api.state,
            'case_list': api.case_list,
            'pass_rate': api.pass_rate,
            'msg_type': api.msg_type,
            'receiver': api.receiver,
            'user': request.user
        }
        try:
            return request_body
        except (Exception,):
            raise Exception("解析测试计划失败 ❌")

    @classmethod
    @database_sync_to_async
    def create_or_update_plan(cls, request: Any, pk: int) -> int:
        """创建或更新测试计划，并根据计划信息添加或移除调度任务。"""

        try:
            request_body = cls.parser_plan_data(request, pk=pk)

            if pk:
                plan = Plan.objects.filter(id=pk).update(**request_body)
                Scheduler.remove(pk)
                Scheduler.add_test_plan(
                    plan.case_list, plan.id, plan.cron
                )
                update_pk = pk
            else:
                plan = Plan.objects.create(**request_body)
                Scheduler.add_test_plan(
                    plan.case_list, plan.id, plan.cron
                )
                update_pk = plan.id

            return update_pk

        except Exception as e:
            raise Exception(f"创建或更新测试计划失败: {e} ❌")

    @classmethod
    def update_test_plan_state(cls, plan_id: int, target_state: int) -> Any:
        """更新测试计划状态，并根据状态添加或移除调度任务。"""

        try:
            plan = Plan.objects.get(pk=plan_id)
            plan_parser_data = cls.parser_plan_data(model_to_dict(plan), pk=plan_id)

            if plan is None:
                raise Exception("测试计划不存在 ❌")

            if plan.state == target_state:
                return ResponseStandard.resp_400()

            if target_state == 1:
                Scheduler.add_test_plan(
                    plan_parser_data.get("case_list", []), plan.id, plan_parser_data.get("cron", "")
                )
            else:
                Scheduler.remove(plan_id)

            plan.state = target_state
            plan.save()
            return ResponseStandard.success()

        except Exception as e:
            raise Exception(f"更新测试计划状态失败: {e} ❌")

    @classmethod
    def run_test_plan(cls, plan_id, case_list):

        plan = Plan.objects.get(pk=plan_id)
        if plan is None:
            raise Exception(f"测试计划: [{plan_id}]不存在 ❌")
        try:
            # 设置为running
            cls.update_test_plan_state(plan_id, 1)
            response = HttpDao.run_test_suite(case_list)
            return response
        except Exception as e:
            raise Exception(f"执行测试计划: 【{plan.name}】失败: {str(e)} ❌")
