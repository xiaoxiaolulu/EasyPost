from protos import executor_pb2
from utils.logger import logger


class Parser:

    @staticmethod
    def parser_report_main(responses, result_list):
        """
        Parses a report data list and populates the 'responses' object with relevant information.

        Args:
            responses (object): The object to store the parsed report data.
            result_list (dict): The dictionary containing the report data.

        Raises:
            Exception: If there's an error during parsing.
        """
        try:
            responses.all = result_list.get("all", 0)
            responses.success = result_list.get("success", 0)
            responses.error = result_list.get("error", 0)
            responses.fail = result_list.get("fail", 0)
            responses.runtime = result_list.get("runtime", "")
            responses.argtime = result_list.get("argtime", "")
            responses.begin_time = result_list.get("begin_time", "")
            responses.pass_rate = result_list.get("pass_rate", "")
            responses.state = result_list.get("state", "")
            responses.tester = result_list.get("tester", "")
        except Exception as err:
            logger.error(f"解析报告数据失败 -> {err}")
            raise Exception("解析报告数据失败❌")

    @classmethod
    def create_report_detail(cls, class_item, class_collection, cases_collection):
        """
        Creates a detailed report for a given class.

        Args:
            cls: The current class object.
            class_item: A dictionary containing class information.
            class_collection: A list to store class details.
            cases_collection: A collection of test cases.

        Returns:
            The updated class_collection list.

        Raises:
            Exception: If an error occurs during report creation.
        """
        try:
            class_data = executor_pb2.ClassList(
                name=class_item.get('name', 'Demo'),
                state=class_item.get('state', 0),
                all=class_item.get('all', 0),
                success=class_item.get('success', 0),
                error=class_item.get('error', 0),
                fail=class_item.get('fail', 0),
                cases=cls.create_detail_step(class_item, cases_collection)
            )
            class_collection.append(class_data)
            return class_collection
        except Exception as err:
            logger.error(f"创建报告详情失败 -> {err}")
            raise Exception("创建报告详情失败❌")

    @staticmethod
    def create_detail_step(class_item, cases_collection):
        """
          Creates detailed step information for a given class.

          Args:
              class_item: A dictionary containing class information, including a list of cases.
              cases_collection: A list to store case details.

          Returns:
              The updated cases_collection list.

          Raises:
              Exception: If an error occurs during step creation.
        """
        try:
            for index, case_item in enumerate(class_item.get('cases', [])):
                cases_collection.append(executor_pb2.Cases(
                    name=case_item.get('name', 'Demo'),
                    log_data=case_item.get('log_data', []),
                    l_env=case_item.get('l_env', []),
                    g_env=case_item.get('g_env', []),
                    hook_gen=str(case_item.get('hook_gen', [])),
                    url=case_item.get('url', ''),
                    method=case_item.get('method', ''),
                    status_code=case_item.get("status_code", 200),
                    content_length=case_item.get('content_length', 0),
                    content_type=case_item.get('content_type', ''),
                    performance_figure=case_item.get('performance_figure', ''),
                    requests_header=case_item.get("requests_header", ''),
                    response_body=case_item.get('response_body', ''),
                    count=case_item.get('count', 0),
                    state=case_item.get('state', ''),
                    tag=case_item.get('tag', ''),
                    run_time=case_item.get('run_time', ''),
                    validate_extractor=case_item.get('validate_extractor', '')
                ))
                return cases_collection
        except Exception as err:
            logger.error(f"创建报告详情步骤数据失败 -> {err}")
            raise Exception("创建报告详情步骤数据失败❌")

    @classmethod
    def create_report(cls, result_list, responses):
        """
        Creates a test report based on the provided result list.

        Args:
            cls: The current class object.
            result_list: A dictionary containing test results.
            responses: An object to store the generated report data.

        Returns:
            The updated responses object.

        Raises:
            Exception: If an error occurs during report creation.
        """
        try:
            cls.parser_report_main(responses, result_list)

            class_collection, cases_collection = list(), list()

            for class_item in result_list.get('class_list', []):
                cls.create_report_detail(class_item, class_collection, cases_collection)

            responses.class_list.extend(class_collection)

            return responses
        except Exception as err:
            logger.debug(
                f"🏓生成测试报告失败 -> {err}"
            )
            raise Exception(f"{err} ❌")
