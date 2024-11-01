"""
DESCRIPTION：测试计划数据访问对象
:Created by Null.
"""
from typing import Any
from channels.db import database_sync_to_async
from django.forms import model_to_dict
from api.dao.https import HttpDao
from api.emus.PlanEnum import PlanType
from api.models.plan import Plan
from api.models.project import Project
from api.response.fatcory import ResponseStandard
from api.scheduler.scheduler import Scheduler
from common.process.parser import HandelTestData
from utils.logger import logger


class PlanDao:

    @staticmethod
    def parser_plan_data(request: Any, pk=None):
        """
        Parses test plan data from a process object and project ID (optional for update).

        Args:
            request: The Django process object containing the data to be parsed.
            pk (int, optional): The primary key of the plan for update (if provided).

        Returns:
            A dictionary containing the parsed test plan data.

        Raises:
            Exception: If an error occurs during data parsing.
        """
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
        except (Exception,) as err:
            logger.debug(
                f"🎯解析测试计划数据失败 -> {err}"
            )
            raise Exception("解析测试计划失败 ❌")

    @classmethod
    @database_sync_to_async
    def create_or_update_plan(cls, request: Any, pk: int) -> int:
        """
        Creates a new test plan or updates an existing one based on the provided data.

        Args:
            request: The Django process object containing the data to be used.
            pk (int): The primary key of the plan to update (if provided).

        Returns:
            The primary key of the created or updated plan (int).

        Raises:
            Exception: If an error occurs during plan creation or update.
        """
        try:
            request_body = cls.parser_plan_data(request, pk=pk)

            if pk:
                plan = Plan.objects.filter(id=pk).update(**request_body)
                Scheduler.remove(pk)
                Scheduler.add_test_plan(
                    case_list=plan.case_list,
                    plan_id=plan.id,
                    plan_name=plan.name,
                    cron=plan.cron
                )
                update_pk = pk
            else:
                plan = Plan.objects.create(**request_body)
                Scheduler.add_test_plan(
                    case_list=plan.case_list,
                    plan_id=plan.id,
                    plan_name=plan.name,
                    cron=plan.cron
                )
                update_pk = plan.id

            return update_pk

        except Exception as e:
            logger.debug(
                f"🎯编辑测试计划数据失败 -> {e}"
            )
            raise Exception(f"创建或更新测试计划失败: {e} ❌")

    @classmethod
    def update_test_plan_state(cls, plan_id: int, target_state: int) -> Any:
        """
        Updates the state of a test plan.

        Args:
            plan_id (int): The ID of the plan to update.
            target_state (int): The target state to set for the plan.

        Returns:
            A response object indicating success or failure.

        Raises:
            Exception: If an error occurs during state update.
        """
        try:
            plan = Plan.objects.get(pk=plan_id)
            plan_parser_data = cls.parser_plan_data(model_to_dict(plan), pk=plan_id)

            if plan is None:
                raise Exception("测试计划不存在 ❌")

            if plan.state == target_state:
                return ResponseStandard.resp_400()

            if target_state == PlanType.START:
                Scheduler.add_test_plan(
                    plan_parser_data.get("case_list", []),
                    plan.name,
                    plan.id,
                    plan_parser_data.get("cron", "")
                )
            else:
                Scheduler.remove(plan_id)

            plan.state = target_state
            plan.save()
            return ResponseStandard.success()

        except Exception as e:
            logger.debug(
                f"🎯更新测试计划数据失败 -> {e}"
            )
            raise Exception(f"更新测试计划状态失败: {e} ❌")

    @classmethod
    def run_test_plan(cls, plan_id, case_list):
        """
        Executes a test plan and returns the response from the test suite.

        Args:
            plan_id (int): The ID of the plan to execute.
            case_list (list): A list of case IDs to be included in the execution.

        Returns:
            The response object from the test suite.

        Raises:
            Exception: If an error occurs during plan execution.
        """
        plan = Plan.objects.get(pk=plan_id)
        if plan is None:
            raise Exception(f"测试计划: [{plan_id}]不存在 ❌")
        try:

            cls.update_test_plan_state(plan_id, 1)
            response = HttpDao.run_test_suite(case_list)
            return response
        except Exception as e:
            logger.debug(
                f"🎯执行测试计划失败 -> {e}"
            )
            raise Exception(f"执行测试计划: 【{plan.name}】失败: {str(e)} ❌")
