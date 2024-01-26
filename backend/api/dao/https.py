from typing import (
    Any,
    List
)
from django.forms import model_to_dict
from api.models.https import (
    Relation,
    Api,
    Case,
    Step
)
from api.models.project import Project
from core.engine.session_runner import (
    run_test,
    run_api
)
from core.request.parser import HandelTestData
from utils.trees import (
    collections_directory_id,
    get_relation_tree
)


class HttpDao:

    @staticmethod
    def get_directory_tree(project_id: int):
        """
        获取指定项目的目录树。

        Args:
            project_id: 项目 ID

        Returns:
            目录树字典

        Raises:
            Exception: 获取目录树失败时抛出异常
        """
        try:
            tree = Relation.objects.get(project__id=project_id)
            tree = eval(tree.tree)
            return tree
        except (Relation.DoesNotExist, Exception):
            raise Exception("获取目录详情失败")

    @staticmethod
    def get_directory_case(get_queryset, project_id: int):
        """
        获取指定项目下的所有测试用例。

        Args:
            get_queryset: 获取测试用例的查询集
            project_id: 项目 ID

        Returns:
            测试用例查询集

        Raises:
            Exception: 获取测试用例失败时抛出异常
        """
        try:
            queryset = get_queryset.filter(project__id=project_id).order_by('-update_time')
            return queryset
        except (Api.DoesNotExist, Exception):
            raise Exception("获取测试接口失败")

    @classmethod
    def list_test_case(cls, get_queryset, node: Any, project_id: Any, name: str = ""):
        # Early return if project_id or node is not provided
        if not project_id:
            _queryset = get_queryset.order_by('-update_time')
            if name:
                _queryset = get_queryset.filter(name=name)
            return _queryset
        else:
            try:
                queryset = cls.get_directory_case(get_queryset, project_id)
                tree = cls.get_directory_tree(project_id)
                node = int(node)

                if node == 1:
                    pass  # queryset remains unchanged for root node
                else:
                    children_tree = get_relation_tree(tree, node)
                    directory_ids = collections_directory_id(children_tree, node)
                    queryset = queryset.filter(project__id=project_id, directory_id__in=directory_ids)

                if name:
                    queryset = queryset.filter(name=name)

                return queryset

            except (Api.DoesNotExist, Exception) as e:
                raise Exception("获取测试接口失败") from e

    @staticmethod
    def parser_api_data(request: Any, pk=None):
        """
        解析 API 文档数据，并根据是否更新操作进行处理。

        Args:
            request: HTTP 请求对象
            pk: API 文档 ID（用于更新操作）

        Returns:
            用于创建或更新 API 文档的字典

        Raises:
            Exception: 解析 API 文档失败时抛出异常
        """
        api = HandelTestData(request.data)  # noqa

        if pk:
            update_obj = Api.objects.get(id=pk)
            project = update_obj.project
            directory_id = update_obj.directory_id
        else:
            project = Project.objects.get(id=api.project)
            directory_id = api.directory_id

        request_body = {
            'name': api.name,
            'project': project,
            'directory_id': directory_id,
            'method': api.method,
            'url': api.url,
            'priority': api.priority,
            'status': api.status,
            'desc': api.desc,
            'headers': api.headers,
            'raw': api.raw,
            'params': api.params,
            'setup_script': api.setup_script,
            'teardown_script': api.teardown_script,
            'validate': api.validate,
            'extract': api.extract,
            'user': request.user
        }
        try:
            return request_body
        except (Exception,):
            raise Exception("解析测试接口失败")

    @classmethod
    def create_or_update_api(cls, request: Any, pk):
        """
        创建或更新 API 文档。

        Args:
            request: HTTP 请求对象
            pk: API 文档 ID（用于更新操作）

        Returns:
            创建或更新后的 API 文档 ID

        Raises:
            Exception: 创建或更新 API 文档失败时抛出异常
        """
        try:

            if pk:
                update_obj = Api.objects.filter(id=pk)
                request_body = cls.parser_api_data(request, pk=pk)
                update_obj.update(**request_body)
                update_pk = pk
            else:
                request_body = cls.parser_api_data(request)
                create_obj = Api.objects.create(**request_body)
                update_pk = create_obj.id

            return update_pk
        except Exception as e:
            raise Exception(f"{e}")

    @classmethod
    def run_api_doc(cls, api: dict):
        """
        运行 API 文档。

        Args:
            api: API 文档字典

        Returns:
            测试结果

        Raises:
            Exception: 调试测试接口失败时抛出异常
        """
        try:
            api = HandelTestData(api)
            api_data = api.get_api_template()
            result = run_api(api_data=api_data)
            return result
        except Exception as e:
            raise Exception(f"调试测试接口失败: {e}")

    @staticmethod
    def remove_unwanted_keys(step):
        """
        去除步骤字典中不需要的键。

        Args:
            step: 步骤字典
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
        创建测试用例步骤。

        Args:
            case_obj: 测试用例 ID
            steps: 测试用例步骤列表
        """
        for sort, step in enumerate(steps):
            cls.remove_unwanted_keys(step)
            Step.objects.create(
                sort=sort,
                case_id=case_obj,
                **step
            )

    @classmethod
    def create_or_update_case(cls, request, pk=None):
        """
        创建或更新测试用例。

        Args:
            request: HTTP 请求对象
            pk: 要更新的测试用例 ID（可选）

        Returns:
            更新或创建的测试用例 ID

        Raises:
            Exception: 创建或更新测试用例失败时抛出异常
        """
        try:
            if pk:
                case_obj = Case.objects.filter(id=pk)
                if not case_obj:
                    raise ValueError("Case with given ID does not exist.")

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
        except Exception as e:
            raise Exception(f"{e}")

    @staticmethod
    def parser_case_data(request: Any, pk=None):
        """
        解析测试用例数据，并根据是否更新操作进行处理。

        Args:
            request: HTTP 请求对象
            pk: 要更新的测试用例 ID（可选）

        Returns:
            元组，包含：
                - 用于更新或创建测试用例的字典
                - 测试用例步骤列表

        Raises:
            Exception: 解析测试用例失败时抛出异常
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
        except (Exception,):
            raise Exception("解析测试用例失败")

    @classmethod
    def run_case_steps(cls, data: dict):
        """
        运行单个测试用例的步骤。

        Args:
            data: 包含测试用例信息的字典，包括：
                - step_data: 测试用例步骤列表
                - name: 测试用例名称（可选）

        Returns:
            测试结果

        Raises:
            Exception: 调试测试用例失败时抛出异常
        """
        try:
            runner = HandelTestData()
            steps = data.get('step_data', [])
            name = data.get('name', 'Demo')
            case_data = runner.get_case_template(steps, name)
            result = run_test(case_data)
            return result
        except Exception as e:
            raise Exception(f"调试测试用例失败: {e}")

    @classmethod
    def get_case_list(cls, case_list: List[int]) -> List[dict]:
        """
        获取指定的测试用例列表，并格式化为测试计划所需的格式。

        Args:
            case_list: 测试用例的 ID 列表

        Returns:
            格式化后的测试用例列表
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
        获取格式化后的测试用例步骤列表。

        Args:
            steps: 原始的测试用例步骤列表

        Returns:
            格式化后的测试用例步骤列表
        """
        collections: list = []
        for sort, step in enumerate(steps):
            step = model_to_dict(step)
            cls.remove_unwanted_keys(step)
            collections.append(step)

        return collections

    @classmethod
    def run_test_suite(cls, case: list):
        """
        运行测试套件，执行一组测试用例。

        Args:
            case: 要执行的测试用例列表

        Returns:
            测试结果

        Raises:
            Exception: 调试测试计划失败时抛出异常
        """
        try:
            runner = HandelTestData()
            case_list = cls.get_case_list(case)
            case_data = runner.get_plan_template(case_list)
            result = run_test(case_data)
            return result
        except Exception as e:
            raise Exception(f"调试测试计划失败: {e}")
