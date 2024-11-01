"""
DESCRIPTION：接口测试数据访问对象
:Created by Null.
"""
import asyncio
import json
from typing import (
    Any,
    List
)
from channels.db import database_sync_to_async
from django.db.models import (
    Q,
    Model
)
from django.forms import model_to_dict
from google.protobuf.json_format import MessageToDict
from api.dao import executor_service_client
from api.dao.report import ReportDao
from api.emus import treesEnum
from api.emus.HttpEnum import (
    ApiSnapshotEnum,
    TreeEnum
)
from api.models.https import (
    Relation,
    Case,
    Step,
    ApiCopy
)
from api.models.project import Project
from common.process.parser import HandelTestData
from common.attach.decorator import lock
from utils.logger import logger
from common.process.trees import (
    collections_directory_id,
    get_relation_tree
)


class HttpDao:

    @staticmethod
    def get_directory_tree(project_id: int, type: Any = 0):
        """
        Retrieves the directory tree for a given project and type.

        Args:
            project_id (int): The ID of the project.
            type (int, optional): The type of directory (default: 0).

        Returns:
            A dictionary representing the directory tree.

        Raises:
            Exception: If an error occurs while retrieving the tree.
        """
        try:
            tree = Relation.objects.filter(Q(project__id=project_id) & Q(type=type)).first()
            tree = eval(tree.tree)
            return tree
        except (Relation.DoesNotExist, Exception) as err:
            logger.debug(
                f"🏓获取项目关联的树形结构数据 -> {err}"
            )
            raise Exception("获取目录详情失败❌")

    @staticmethod
    def get_directory_case(get_queryset, project_id: int):
        """
        Retrieves the directory-related test cases for a given project.

        Args:
            get_queryset: The queryset to filter.
            project_id (int): The ID of the project.

        Returns:
            A queryset containing the filtered test cases.

        Raises:
            Exception: If an error occurs while retrieving the cases.
        """
        try:
            queryset = get_queryset.filter(project__id=project_id).order_by('-update_time')
            return queryset
        except Exception as err:
            logger.debug(
                f"🏓获取项目关联的接口数据失败 -> {err}"
            )
            raise Exception("获取测试接口失败❌")

    @classmethod
    def list_test_case(cls, get_queryset, node: Any, project_id: Any, name: str = ""):
        """
        Retrieves a queryset of test cases based on project, directory, and name filters.

        Args:
            get_queryset: The queryset to filter.
            node (Any): The ID of the directory node to filter by (optional).
            project_id (Any): The ID of the project to filter by (optional).
            name (str, optional): The name of the test case to filter by. Defaults to "".

        Returns:
            A filtered queryset of test cases.

        Raises:
            Exception: If an error occurs while retrieving the test cases.
        """
        # Early return if project_id or node is not provided
        if not project_id:
            _queryset = get_queryset.order_by('-update_time')
            if name:
                _queryset = get_queryset.filter(name=name)
            return _queryset
        else:
            try:
                queryset = cls.get_directory_case(get_queryset, project_id)
                tree = cls.get_directory_tree(project_id, treesEnum.TreeType.API)
                node = int(node)

                if node == TreeEnum.current:
                    pass  # queryset remains unchanged for root node
                else:
                    children_tree = get_relation_tree(tree, node)
                    directory_ids = collections_directory_id(children_tree, node)
                    queryset = queryset.filter(project__id=project_id, directory_id__in=directory_ids)

                if name:
                    queryset = queryset.filter(name=name)

                return queryset

            except Exception as err:
                logger.debug(
                    f"🏓获取测试接口数据失败 -> {err}"
                )
                raise Exception(f"获取测试接口失败❌ {err}")

    @staticmethod
    def parser_api_data_pattern(models, project, directory_id, handel, request) -> dict:
        """
        Parses API data from a model instance (`models`), project, directory ID, handler object (`handel`), and process object (`process`).

        Args:
            models: The model class representing the API data.
            project: The project name associated with the API data.
            directory_id: The directory ID for the API data (if applicable).
            handel: A handler object containing various API data attributes.
            request: The process object containing user information.

        Returns:
            A dictionary containing the parsed API data.
        """

        table_name = models._meta.model_name

        request_body = {
            "name": handel.name,
            "method": handel.method,
            "url": handel.url,
            "priority": handel.priority,
            "status": handel.status,
            "desc": handel.desc,
            "headers": handel.headers,
            "raw": handel.raw,
            "params": handel.params,
            "setup_script": handel.setup_script,
            "teardown_script": handel.teardown_script,
            "validate": handel.validate,
            "extract": handel.extract,
            "user": request.user,
            **(
                {
                    "project": project,
                    "directory_id": directory_id,
                }
                if table_name != "step"
                else {}
            ),
        }

        return request_body

    @classmethod
    def parser_api_data(cls, request: Any, pk=None, models=None):
        """
        Parses test API data from a process object and project ID (optional for update).

        Args:
            request: The Django process object containing the data to be parsed.
            pk (int, optional): The primary key of the API object for update (if provided).
            models
        Returns:
            A dictionary containing the parsed test API data.

        Raises:
            Exception: If an error occurs during data parsing.
        """
        api = HandelTestData(request.data)  # noqa
        project = None
        directory_id = None

        try:
            if pk:
                update_obj = models.objects.get(id=pk)
                project = getattr(update_obj, 'project', None)
                directory_id = getattr(update_obj, 'directory_id', None)
            else:
                project = models.objects.get(id=api.project)
                directory_id = api.directory_id

        except (Exception, models.DoesNotExist):
            # 当添加测试步骤 在接口面板中保存, 根据当前的接口主键查询不到数据,
            # 则重新构建步骤的参数, 将数据存储在步骤表中
            pass

        request_body = cls.parser_api_data_pattern(models, project, directory_id, api, request)

        return request_body

    @classmethod
    def create_or_update_api(cls, request: Any, pk, models: Model):
        """
        Creates a new API object or updates an existing one based on provided data.

        Args:
            request: The Django process object containing the API data.
            pk (int): The primary key of the API object to update (if provided).
            models:

        Returns:
            The ID of the created or updated API object.

        Raises:
            Exception: If an error occurs during API creation or update.
        """
        try:

            if pk:
                update_pk = cls.update_api_or_step(pk, models, request)
            else:
                update_pk = cls.create_api_or_step(request, models)

            return update_pk
        except (Exception, models.DoesNotExist):
            update_pk = cls.create_api_or_step(request, models)
            return update_pk

        except Exception as err:
            logger.debug(
                f"🏓编辑测试接口数据失败 -> {err}"
            )
            raise Exception(f"{err} ❌")

    @classmethod
    def update_api_or_step(cls, pk, models, request):
        """
           Updates an existing API object or creates a new one if it doesn't exist.

           Args:
               pk: The primary key of the API object to update.
               models: The model class representing the API object.
               request: The Django process object containing the data to be updated.

           Returns:
               The primary key of the updated or created API object.

           Raises:
               ObjectDoesNotExist: If the API object with the given PK doesn't exist.
               Exception: If an error occurs during the update or creation process.
        """
        try:
            obj = models.objects.filter(id=pk)
            request_body = cls.parser_api_data(request, pk=pk, models=models)
            for key, value in request_body.items():
                setattr(obj, key, value)
            obj.save()
            return pk
        except models.DoesNotExist:
            return cls.create_api_or_step(request, models)

    @classmethod
    def create_api_or_step(cls, request, models):
        """
           Creates a new API object or step in the specified model, handling potential validation errors.

           Args:
               cls: The class representing the current implementation.
               request: The Django process object containing the data to be parsed.
               models: The model class for the API object or step (e.g., models.API or models.Step).

           Returns:
               The primary key of the newly created object.

           Raises:
               ValidationError: If data validation fails during creation.
               Exception: If a generic error occurs during creation.
        """

        try:
            request_body = cls.parser_api_data(request, models=models)
            create_obj = models.objects.create(**request_body)
            update_pk = create_obj.id

            return update_pk
        except (models.DoesNotExist, Exception):

            raise Exception(f"创建测试步骤或接口失败!")

    @classmethod
    async def run_api_doc(cls, api: dict):
        """
        Runs an API test case based on the provided API data.

        Args:
            api (dict): A dictionary containing the API data.

        Returns:
            The response object from the API test run.

        Raises:
            Exception: If an error occurs during the API test run.
        """
        try:
            api = HandelTestData(api)
            api_data = api.get_api_template()
            result = await executor_service_client.run_api_doc(api_data)
            return result
        except Exception as err:
            logger.debug(
                f"🏓调试测试接口数据失败 -> {err}"
            )
            raise Exception(f"调试测试接口失败: {err} ❌")

    @staticmethod
    def remove_unwanted_keys(step):
        """
        Removes unwanted keys from a dictionary containing test step data.

        Args:
            step (dict): The dictionary representing a test step.

        Returns:
            The modified dictionary with unwanted keys removed.
        """
        keys_to_pop = [
            "id",
            "user",
            "directory_id",
            "priority",
            "status",
            "project",
            "case",
            "sort",
            "create_time",
            "update_time"
        ]
        for key in keys_to_pop:
            if key in step:
                del step[key]

    @classmethod
    def create_case_step(cls, case_obj, steps):
        """
        Creates test case steps from a list of step data and associates them with a test case object.

        Args:
            case_obj (object): The test case object to associate the steps with.
            steps (list): A list of dictionaries containing step data.
        """

        for sort, step in enumerate(steps):
            cls.remove_unwanted_keys(step)
            Step.objects.create(
                sort=sort,
                case_id=case_obj,
                **step
            )

    @classmethod
    def delete_case(cls, pk=None):
        """
        Deletes a test case and its associated test steps.

        Args:
            pk (int): The primary key of the test case to delete.

        Raises:
            Exception: If an error occurs during test case deletion.
        """
        try:
            Case.objects.filter(id=pk).delete()
            steps_obj = Step.objects.filter(case__id=pk)
            if steps_obj:
                steps_obj.delete()
        except Exception as err:
            logger.debug(
                f"🏓删除用例数据失败 -> {err}"
            )
            raise Exception(f"{err} ❌")

    @classmethod
    def create_or_update_case(cls, request, pk=None):
        """
        Creates a new test case or updates an existing one based on provided data and associated steps.

        Args:
            request (Any): The Django process object containing the case data.
            pk (int, optional): The primary key of the test case to update (if provided).

        Returns:
            The ID of the created or updated test case.

        Raises:
            ValueError: If a case update is attempted with a non-existent ID.
            Exception: If an error occurs during test case creation or update.
        """
        try:
            if pk:
                case_obj = Case.objects.filter(id=pk)
                if not case_obj:
                    raise ValueError("Case with given ID does not exist. ❌")

                cased_body, steps = cls.parser_case_data(request, pk=pk)
                case_obj.update(**cased_body)
                steps_obj = Step.objects.filter(case__id=pk)

                if steps_obj:
                    steps_obj.delete()
                cls.create_case_step(pk, steps)
                update_pk = pk

            else:
                cased_body, steps = cls.parser_case_data(request)
                case_obj = Case.objects.create(**cased_body)
                cls.create_case_step(case_obj.id, steps)
                update_pk = case_obj.id

            return update_pk
        except Exception as err:
            logger.debug(
                f"🏓更新用例数据失败 -> {err}"
            )
            raise Exception(f"{err} ❌")

    @staticmethod
    def parser_case_data(request: Any, pk=None):
        """
        Parses test case data and associated step data from a process object.

        Args:
            request (Any): The Django process object containing the test case data.
            pk (int, optional): The primary key of the test case to update (if provided).

        Returns:
            A tuple containing:
                - request_body (dict): A dictionary containing the parsed test case data.
                - step_data (list): A list containing the parsed step data (assumed to be handled by HandelTestData).

        Raises:
            Exception: If an error occurs during data parsing.
        """
        api = HandelTestData(request.data)  # noqa

        if pk:
            update_obj = Case.objects.get(id=pk)
            project = update_obj.project
            directory_id = update_obj.directory_id
        else:
            project = Project.objects.get(id=api.project)
            directory_id = api.directory_id

        request_body = {
            'name': api.name,
            'project': project,
            'directory_id': directory_id,
            'priority': api.priority,
            'desc': api.desc,
            'user': request.user
        }
        try:
            return request_body, api.step_data
        except (Exception,) as err:
            logger.debug(
                f"🏓解析测试用例数据失败 -> {err}"
            )
            raise Exception("解析测试用例失败 ❌")

    @classmethod
    async def run_case_steps(cls, data: dict):
        """
        Runs a test case based on the provided data and associated step data.

        Args:
            data (dict): A dictionary containing the test case data and step data.

        Returns:
            The response object from the test case run.

        Raises:
            Exception: If an error occurs during the test case run.
        """
        try:
            runner = HandelTestData()
            steps = data.get('step_data', [])
            name = data.get('name', 'Demo')
            case_data = runner.get_case_template(steps, name)
            result = await executor_service_client.run_case(case_data)
            return result
        except Exception as e:
            logger.debug(
                f"🏓调试用例数据失败 -> {e}"
            )
            raise Exception(f"调试测试用例失败: {e} ❌")

    @classmethod
    def get_case_list(cls, case_list: List[int]) -> List[dict]:
        """
        Retrieves a list of test case details and associated steps.

        Args:
            case_list (List[int]): A list of test case IDs.

        Returns:
            A list of dictionaries containing test case details and step information.

        Raises:
            ValueError: If no test cases are found with the provided IDs.
        """
        case_object = Case.objects.filter(id__in=case_list).values("id", "name")
        collections = [{
            "name": suite["name"],
            "cases": cls.get_case_step(Step.objects.filter(case_id=suite["id"]).all())
        } for suite in case_object]

        return collections

    @classmethod
    def get_case_step(cls, steps: List[dict]) -> List[dict]:
        """
        Processes a list of step objects, removing unwanted keys and converting them to serializable dictionaries.

        Args:
            steps (List[dict]): A list of step objects (likely model instances).

        Returns:
            A list of cleaned dictionaries containing step data.
        """
        collections: list = []
        for sort, step in enumerate(steps):
            step = model_to_dict(step)
            cls.remove_unwanted_keys(step)
            collections.append(step)

        return collections

    @classmethod
    @lock("plan")
    def run_test_suite(cls, case: list, report_name=None):
        """
        Runs a test suite based on a provided list of test cases and generates a report.

        Args:
            case (list): A list of test case IDs.
            report_name (str, optional): The name for the generated report.

        Returns:
            The test run response object.

        Raises:
            Exception: If an error occurs during test execution or report generation.
        """
        try:
            runner = HandelTestData()
            case_list = cls.get_case_list(case)
            case_data = runner.get_plan_template(case_list)

            result = asyncio.run(executor_service_client.run_plan(case_data))
            result = MessageToDict(result)

            logger.debug(f"--------  response info ----------\n")
            logger.debug(json.dumps(dict(result), ensure_ascii=False, indent=4))
            logger.debug(f"--------  response info ----------\n")

            ReportDao.create_report(
                plan_name=report_name,
                result_list=result
            )
            return result
        except Exception as e:
            logger.debug(
                f"🏓调试测试计划失败 -> {e}"
            )
            raise Exception(f"调试测试计划失败: {e} ❌")

    @classmethod
    @database_sync_to_async
    def create_api_snapshot(cls, request: Any):
        """
        Creates an API snapshot asynchronously, managing a maximum of 100 snapshots per user.

        Args:
            request (Any): The process object containing API data.

        Raises:
            Exception: If an error occurs during snapshot creation.
        """
        try:
            request_body = cls.parser_api_data(request)
            api_copy_records = ApiCopy.objects.filter(user=request.user).order_by('-create_time')

            if len(api_copy_records) > ApiSnapshotEnum.numbers:
                oldest_record = api_copy_records[ApiSnapshotEnum.numbers]
                ApiCopy.objects.filter(user=request.user).filter(
                    create_time__lt=oldest_record.create_time).delete()

            ApiCopy.objects.create(**request_body)
        except Exception as e:
            logger.debug(
                f"🏓创建接口快照失败 {e}"
            )
            raise Exception(f"{e} ❌")

    # @staticmethod
    # def import_api_docs(process, pk, filepath, files, import_type):
    #
    #     if not pk:
    #         raise ValueError("Invalid api docs PK provided.")
    #
    #     if not import_type:
    #         raise ValueError("Invalid import type provided.")
    #
    #     try:
    #         if not os.path.exists(filepath):
    #             raise FileExistsError(f"File not exists: {filepath}")
    #
    #         with open(filepath, 'wb+') as f:
    #             for chunk in files.chunks():
    #                 f.write(chunk)
    #
    #         # More specific object retrieval based on import_type
    #         import_objects = EventManager.map.get(import_type)
    #         if not import_objects:
    #             raise ValueError(f"Invalid import type: {import_type}")
    #
    #         migrator = DataMigrator(import_objects, UitRunnerSource())
    #         migrator.migrate(filename=filepath, process=process, pk=pk, type=import_type)
    #
    #     except (FileNotFoundError, PermissionError, FileExistsError) as e:
    #         logger.error(f"{e}")
    #         raise ValueError(f"An error occurred during import: {e}")
