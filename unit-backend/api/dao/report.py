"""
DESCRIPTION：测试报告数据访问对象
:Created by Null.
"""
import sys

from api.models.report import (
    Main,
    Detail,
    DetailStep
)
from utils.logger import logger


class ReportDao:

    """
    Test report Details

    📒report-main Test report master data (shown in the list and report details body)
        |
        |
        |---📑case - the detail test report show scenes (test plan specified operation cases)
                |
                |
                |---📃step - the detail test scenario includes the steps of interface information for details
    """

    @classmethod
    def detail_step_list(cls, get_queryset, report_id, name: str = ""):
        """
        Retrieves a list of step details for a given test report.

        Args:
            get_queryset: The queryset to use for filtering.
            report_id: The ID of the test report to get step details for.
            name: An optional filter to only return steps with the specified name.

        Returns:
            A queryset of step details.

        Raises:
            Exception: If the report ID is missing or an error occurs while retrieving the data.
        """
        if not report_id:
            raise Exception("缺少必要参数报告id❌ ")
        else:
            try:
                queryset = get_queryset.filter(report_id=report_id)

                if name:
                    queryset = queryset.filter(name=name)

                return queryset

            except Exception as err:
                logger.debug(
                    f"🏓获取测试报告数据失败 -> {err}"
                )
                raise Exception(f"获取测试报告数据失败❌ {err}")

    @staticmethod
    def parser_report_main(plan_name, result_list):
        """
        Parses and extracts the main report data from the provided result list.

        Args:
            plan_name: The name of the test plan.
            result_list: A list of test result data.

        Returns:
            A dictionary containing the main report data.

        Raises:
            Exception: If an error occurs while parsing the data.
        """
        try:
            resport_main = {
                "name": plan_name,
                **{k: v for k, v in result_list.items() if k in (
                    "state",
                    "all",
                    "success",
                    "error",
                    "fail",
                    "runtime",
                    "begin_time",
                    "argtime",
                    "pass_rate",
                    "tester")
                   }
            }
            return resport_main
        except Exception as err:
            logger.error(f"解析报告数据失败 -> {err}")
            raise Exception("解析报告数据失败❌")

    @staticmethod
    def create_report_detail(model, class_item):
        """
        Creates a new report detail object in the database.

        Args:
            model: An instance of the Main model (assumed to represent the main report).
            class_item: A dictionary containing data for the report detail object.

        Returns:
            The created Detail object on success.

        Raises:
            Exception: If an error occurs while creating the report detail.
        """
        try:
            detail_obj = Detail.objects.create(
                report=Main.objects.get(id=model.id),
                name=class_item.get('name', 'Demo'),
                state=class_item.get('state', 0),
                all=class_item.get('all', 0),
                success=class_item.get('success', 0),
                error=class_item.get('error', 0),
                fail=class_item.get('fail', 0)
            )
            return detail_obj
        except Exception as err:
            logger.error(f"创建报告详情失败 -> {err}")
            raise Exception("创建报告详情失败❌")

    @staticmethod
    def create_detail_step(class_item, model):
        """
        Creates multiple detail step objects in the database based on a list of cases.

        Args:
            class_item: A dictionary containing data about multiple test cases.
            model: An instance of the Detail model representing the parent report detail.

        Raises:
            Exception: If an error occurs while creating the detail steps.
        """
        try:
            for index, case_item in enumerate(class_item.get('cases', [])):

                DetailStep.objects.create(
                    sort=(index + 1),
                    detail=Detail.objects.get(id=model.id),
                    name=case_item.get('name', 'Demo'),
                    log_data=case_item.get('logData', []),
                    url=case_item.get('url', ''),
                    method=case_item.get('method', ''),
                    status_code=case_item.get('statusCode', ''),
                    response_header=case_item.get('responseHeader', ''),
                    requests_header=case_item.get("requestsHeader", ''),
                    response_body=case_item.get('responseBody', ''),
                    requests_body=case_item.get('requestsBody', ''),
                    extras=case_item.get('extras', []),
                    validate_extractor=case_item.get('validateExtractor', []),
                    state=case_item.get('state', ''),
                    run_time=case_item.get('runTime', '')
                )
        except Exception as err:
            logger.error(f"创建报告详情步骤数据失败 -> {err}")
            raise Exception("创建报告详情步骤数据失败❌")

    @classmethod
    def create_report(cls, plan_name, result_list):
        """
        Creates a test report with main data, details, and step details from the provided information.

        Args:
            plan_name: The name of the test plan.
            result_list: A list containing test result data.

        Raises:
            Exception: If an error occurs while creating the report.
        """
        try:
            report_main = cls.parser_report_main(plan_name, result_list)
            report_obj = Main.objects.create(**report_main)
            for class_item in result_list.get('classList', []):
                detail_obj = cls.create_report_detail(report_obj, class_item)
                cls.create_detail_step(class_item, detail_obj)

        except Exception as err:
            logger.debug(
                f"🏓生成测试报告失败 -> {err}"
            )
            raise Exception(f"{err} ❌")
