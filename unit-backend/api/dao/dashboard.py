"""
DESCRIPTION：看板数据访问对象
:Created by Null.
"""
from django.db.models import (
    Avg
)
from api.models.https import (
    Api,
    Case
)
from api.models.plan import Plan
from api.models.report import Main
from api.models.user import User
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
    def get_current_month_count(model):
        """
        Function to retrieve the count of records for the current month in the specified model.

        Parameters:
            model (Model): The Django model class for which to retrieve the count.

        Returns:
            int: The count of records for the current month.

        Raises:
            Exception: If an error occurs while retrieving the count.
        """
        try:
            count = model.objects.filter(create_time__gte=time.month_start(), create_time__lte=time.month_end()).count()
            return count
        except (model.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓 [{str(model)}] 获取本月数据失败 -> {err}"
            )
            raise Exception("获取本月数据失败❌")

    @staticmethod
    def get_previous_month_count(model):
        """
        Function to retrieve the count of records for the previous month in the specified model.

        Parameters:
            model (Model): The Django model class for which to retrieve the count.

        Returns:
            int: The count of records for the previous month, or 0 if an error occurs.
        """
        try:
            count = model.objects.filter(
                create_time__gte=time.get_previous_month_start(),
                create_time__lte=time.get_previous_month_end()
            ).count()
            return count
        except (model.DoesNotExist, Exception):
            return 0

    def increment(self, model):
        """
        Calculates the percentage increment between the current month's count and
        the previous month's count for the specified model.

        This method assumes the presence of `get_current_month_count` and
        `get_previous_month_count` methods (likely within the same class).

        Parameters:
            model (Model): The Django model class for which to calculate the increment.

        Returns:
            str: The percentage increment as a string, or "0%" if an error occurs.
        """
        try:
            increment = ((
                        self.get_current_month_count(model) - self.get_previous_month_count(model))
                         / self.get_previous_month_count(model))
            increment = f"{increment * 100}%"
            return increment
        except (Exception, ZeroDivisionError) as err:
            increment = "0%"
            return increment

    def get_current_month_api_count(self):
        """
        Retrieves the count of API records for the current month.

        This method leverages the `get_current_month_count` function
        , assuming it's defined within the same class or accessible.

        Returns:
            int: The count of API records for the current month.
        """
        count = self.get_current_month_count(Api)
        return count

    def get_previous_month_api_count(self):
        """
        Retrieves the count of API records for the previous month.

        This method leverages the `get_previous_month_count` function
        , assuming it's defined within the same class or accessible.

        Returns:
            int: The count of API records for the previous month.
        """
        count = self.get_previous_month_count(Api)
        return count

    def api_increment(self):
        """
        Calculates the percentage increment between the current
        month's API count and the previous month's API count.

        This method utilizes the `increment` function, assuming
         it's defined within the same class or accessible.

        Returns:
            str: The percentage increment as a string, or "0%" if an error occurs.
        """
        increment = self.increment(Api)
        return increment

    def get_current_month_case_count(self):
        """
        Retrieves the count of case records for the current month.

        This method leverages the `get_current_month_count` function,
         assuming it's defined within the same class or accessible.

        Returns:
            int: The count of case records for the current month.
        """
        count = self.get_current_month_count(Case)
        return count

    def get_previous_month_case_count(self):
        """
        Retrieves the count of case records for the previous month.

        This method leverages the `get_previous_month_count` function,
         assuming it's defined within the same class or accessible.

        Returns:
            int: The count of case records for the previous month.
        """
        count = self.get_previous_month_count(Case)
        return count

    def case_increment(self):
        """
        Calculates the percentage increment between the current
        month's case count and the previous month's case count.

        This method utilizes the `increment` function, assuming
         it's defined within the same class or accessible.

        Returns:
            str: The percentage increment as a string, or "0%" if an error occurs.
        """
        increment = self.increment(Case)
        return increment

    def get_current_month_plan_count(self):
        """
        Retrieves the count of plan records for the current month.

        This method leverages the `get_current_month_count` function,
         assuming it's defined within the same class or accessible.
         It's likely used for tracking or managing plans.

        Returns:
            int: The count of plan records for the current month.
        """
        count = self.get_current_month_count(Plan)
        return count

    def get_previous_month_plan_count(self):
        """
        Retrieves the count of plan records for the previous month.

        This method leverages the `get_previous_month_count` function,
         assuming it's defined within the same class or accessible.
          It's likely used for tracking or managing historical plan data.

        Returns:
            int: The count of plan records for the previous month.
        """
        count = self.get_previous_month_count(Plan)
        return count

    def plan_increment(self):
        """
        Calculates the percentage increment between the current
        month's plan count and the previous month's plan count.

        This method utilizes the `increment` function, assuming
         it's defined within the same class or accessible.

        Returns:
            str: The percentage increment as a string, or "0%" if an error occurs.
        """
        increment = self.increment(Plan)
        return increment

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
    def get_plan_count():
        """
        Retrieves the total count of plan records.

        This method utilizes the `Plan` model's `objects.count()` method to fetch the count.

        Returns:
            int: The total count of plan records.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            count = Plan.objects.count()
            return count
        except (Plan.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取测试计划数据失败 -> {err}"
            )
            raise Exception("获取测试计划数据失败 ❌")

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

    @staticmethod
    def get_last_login(request):
        """
        Retrieves the last login timestamp for the currently logged-in user.

        This function extracts the user's primary key from the process object
        and uses it to fetch the corresponding user record from the `User` model.
        It then returns the `last_login_time` attribute from the retrieved user object.

        Parameters:
            request: The HTTP process object containing user information.

        Returns:
            datetime: The last login timestamp for the current user, or None if an error occurs.

        Raises:
            Exception: If an error occurs during user retrieval or last login timestamp retrieval.
        """

        try:
            last_login = User.objects.get(pk=request.user.pk).last_login_time
            return last_login
        except (User.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取用户最近的登录时间数据失败 -> {err}"
            )
            raise Exception("获取用户最近的登录时间数据失败❌")

    @staticmethod
    def get_user_ip(request):
        """
        Retrieves the IP address associated with the currently logged-in user.

        This function assumes that the `ip_address` field is present on the `User`
         model and that it stores the user's IP address. It extracts the user's
          primary key from the process object and uses it to fetch the corresponding
           user record. It then returns the `ip_address` attribute from the retrieved user object.

        Parameters:
            request: The HTTP process object containing user information.

        Returns:
            str: The IP address associated with the current user, or None if an error occurs.

        Raises:
            Exception: If an error occurs during user retrieval or IP address retrieval.
        """
        try:
            ip_address = User.objects.get(pk=request.user.pk).ip_address
            return ip_address
        except (User.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取用户登录地址数据失败 -> {err}"
            )
            raise Exception("获取用户登录地址数据失败❌")

    @staticmethod
    def get_user_name(request):
        """
        Retrieves the username of the currently logged-in user.

        This function assumes that the `username` attribute is accessible on the process
        object and contains the user's username. It directly returns the `username` attribute.

        Parameters:
            request: The HTTP process object containing user information.

        Returns:
            str: The username of the current user, or None if an error occurs.

        Raises:
            Exception: If an error occurs during username retrieval.
        """
        try:
            user_name = request.user.username
            return user_name
        except(Exception, ) as err:
            logger.debug(
                f"🏓获取用户名数据失败 -> {err}"
            )
            raise Exception("获取用户名数据失败❌")

    def get_unit_statistics(self):
        """
        Retrieves and aggregates various unit statistics for the dashboard.

        This function calls helper methods to retrieve individual statistics such as API count,
         case count, plan count, and their respective increments (percentage changes compared to
          the previous month). It then combines these statistics into a dictionary for easier access and representation.

        Returns:
            dict: A dictionary containing various unit statistics for the dashboard. Keys include:
                - "api_count": Total number of APIs.
                - "api_increment": Percentage change in API count compared to the previous month.
                - "case_count": Total number of test cases.
                - "case_increment": Percentage change in test case count compared to the previous month.
                - "plan_count": Total number of plans.
                - "plan_increment": Percentage change in plan count compared to the previous month.

        Raises:
            Exception: If any errors occur during data retrieval.
        """

        try:
            unit_statistics = {
                "api_count": self.get_api_count(),
                "api_increment": self.api_increment(),
                "case_count": self.get_case_count(),
                "case_increment": self.case_increment(),
                "plan_count": self.get_plan_count(),
                "plan_increment": self.plan_increment()
            }
            return unit_statistics
        except (Exception, ) as err:
            logger.debug(
                f"🏓获取看板数据失败 -> {err}"
            )
            raise Exception("获取看板数据失败❌")

    def summary(self, request=None):
        """
        Generates a summary dictionary containing user and unit statistics for the dashboard.

        This function retrieves various information related to the currently logged-in user
         (if `process` is provided) and unit-level statistics for the dashboard. It calls helper methods to:

        - Get username (if process object is available).
        - Get user's IP address (if process object is available).
        - Get the user's last login timestamp (if process object is available).
        - Retrieve unit statistics like API/case counts and their increments.

        The retrieved information is then combined into a dictionary for easier access and representation.

        Parameters:
            request (optional): The HTTP process object containing user information.

        Returns:
            dict: A dictionary containing user and unit statistics. Keys include:
                - "username": Username of the logged-in user (if process provided).
                - "ip_address": IP address of the logged-in user (if process provided).
                - "last_login": Last login timestamp of the logged-in user (if process provided).
                - "unit_statistics": A dictionary containing various unit statistics for the dashboard
                (refer to `get_unit_statistics` docstring for details).

        Raises:
            Exception: If any errors occur during data retrieval.
        """
        try:
            username = self.get_user_name(request)
            ip_address = self.get_user_ip(request)
            last_login = self.get_last_login(request)
            unit_statistics = self.get_unit_statistics()

            return {
                "username": username,
                "ip_address": ip_address,
                "last_login":  last_login,
                "unit_statistics": unit_statistics
            }
        except (Exception, ) as err:
            logger.debug(
                f"🏓获取看板数据失败 -> {err}"
            )
            raise Exception("获取看板数据失败❌")
