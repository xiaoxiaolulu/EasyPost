"""
DESCRIPTION：看板数据访问对象
:Created by Null.
"""
from django.db.models import Avg
from api.models.https import (
    Api,
    Case
)
from api.models.report import Main
from utils.logger import logger
from utils import time


class DashboardDao:

    @staticmethod
    def get_api_count():

        """
        Retrieves the total number of API documents in the database.

        Returns:
            The total number of API documents.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            count = Api.objects.count()
            return count
        except (Api.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取接口文档数据失败 -> {err}"
            )
            raise Exception("获取接口文档数据失败❌")

    @staticmethod
    def get_ytd_api_count():
        """
        Retrieves the number of API documents created yesterday.

        Returns:
            The number of API documents created yesterday.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            count = Api.objects.filter(create_time__date=time.yesterday).count()
            return count
        except (Api.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取接口文档数据失败 -> {err}"
            )
            raise Exception("获取接口文档数据失败❌")

    @staticmethod
    def get_past_api_count(days=7):
        """
        Retrieves the number of API documents created in the past `days`.

        Args:
            days (int, optional): The number of days to look back. Defaults to 7.

        Returns:
            The number of API documents created in the past `days`.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            count = Api.objects.filter(create_time__date__in=time.get_before_day(days)).count()
            return count
        except (Api.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取接口文档数据失败 -> {err}"
            )
            raise Exception("获取接口文档数据失败❌")

    @staticmethod
    def get_case_count():
        """
        Retrieves the total number of test cases in the database.

        Returns:
            The total number of test cases.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            count = Case.objects.count()
            return count
        except (Case.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取测试用例数据失败 -> {err}"
            )
            raise Exception("获取测试用例数据失败❌")

    @staticmethod
    def get_case_pass_rate():
        """
        Retrieves the average test case pass rate.

        Returns:
            The average test case pass rate.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            pass_rate = Main.objects.aggregate(Avg("pass_rate"))

            return pass_rate
        except (Main.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取测试用例通过率数据失败 -> {err}"
            )
            raise Exception("获取测试用例通过率数据失败❌")

    @staticmethod
    def get_execute_count():
        """
        Retrieves the total number of test case executions.

        Returns:
            The total number of test case executions.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            count = Main.objects.count()
            return count

        except (Main.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取测试用例执行次数据失败 -> {err}"
            )
            raise Exception("获取测试用例执行次数数据失败❌")
