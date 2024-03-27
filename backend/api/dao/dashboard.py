"""
DESCRIPTION：看板数据访问对象
:Created by Null.
"""
from api.models.https import (
    Api,
    Case
)
from utils.logger import logger
from utils import time


class DashboardDao:

    @staticmethod
    def get_api_count():
        """
        获取API文档的数量。

        :return: 返回API文档的数量。
        :rtype: int
        :raises Exception: 当获取数量失败时引发异常。
        """
        try:
            count = Api.objects.count()
            return count
        except (Api.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取接口文档数据数据失败 -> {err}"
            )
            raise Exception("获取接口文档数据数据失败❌")

    @staticmethod
    def get_ytd_api_count():
        """
        获取昨天的API文档的数量。

        :return: 返回API文档的数量。
        :rtype: int
        :raises Exception: 当获取数量失败时引发异常。
        """
        try:
            count = Api.objects.filter(create_time__date=time.yesterday).count()
            return count
        except (Api.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取接口文档数据数据失败 -> {err}"
            )
            raise Exception("获取接口文档数据数据失败❌")

    @staticmethod
    def get_past_api_count(days=7):
        """
        获取过去多少天的API文档的数量。

        :return: 返回API文档的数量。
        :rtype: int
        :raises Exception: 当获取数量失败时引发异常。
        """
        try:
            count = Api.objects.filter(create_time__date__in=time.get_before_day(days)).count()
            return count
        except (Api.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取接口文档数据数据失败 -> {err}"
            )
            raise Exception("获取接口文档数据数据失败❌")

    @staticmethod
    def get_case_count():
        """
        获取测试用例的数量。

        :return: 返回测试用例的数量。
        :rtype: int
        :raises Exception: 当获取数量失败时引发异常。
        """
        try:
            count = Case.objects.count()
            return count
        except (Case.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取测试用例数据数据失败 -> {err}"
            )
            raise Exception("获取测试用例数据数据失败❌")
