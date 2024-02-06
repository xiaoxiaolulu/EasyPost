from api.models.report import (
    Main,
    Detail,
    DetailStep
)
from utils.logger import logger


class ReportDao:

    """
    测试报告详情

    📒report-main  测试报告主数据(展示在列表与报告详情主体)
        |
        |
        |---📑case-detail 测试报告场景展示（测试计划指定运行用例）
                |
                |
                |---📃step-detail 测试场景下包含的步骤执行接口详情信息
    """

    @staticmethod
    def parser_report_main(plan_name, result_list):
        """解析报告主数据"""
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
        try:
            for case_item in class_item.get('cases', []):

                DetailStep.objects.create(
                    detail=Detail.objects.get(id=model.id),
                    name=case_item.get('name', 'Demo'),
                    log_data=case_item.get('log_data', []),
                    url=case_item.get('url', ''),
                    method=case_item.get('method', ''),
                    status_code=case_item.get('status_code', ''),
                    response_header=case_item.get('response_header', ''),
                    requests_header=case_item.get("requests_header", ''),
                    response_body=case_item.get('response_body', ''),
                    requests_body=case_item.get('requests_body', ''),
                    extras=case_item.get('extras', []),
                    validate_extractor=case_item.get('validate_extractor', []),
                    state=case_item.get('state', ''),
                    run_time=case_item.get('run_time', '')
                )
        except Exception as err:
            logger.error(f"创建报告详情步骤数据失败 -> {err}")
            raise Exception("创建报告详情步骤数据失败❌")

    @classmethod
    def create_report(cls, plan_name, result_list):
        try:
            report_main = cls.parser_report_main(plan_name, result_list)
            report_obj = Main.objects.create(**report_main)

            for class_item in result_list.get('class_list', []):
                detail_obj = cls.create_report_detail(report_obj, class_item)
                cls.create_detail_step(class_item, detail_obj)

        except Exception as err:
            logger.debug(
                f"🏓生成测试报告失败 -> {err}"
            )
            raise Exception(f"{err} ❌")
