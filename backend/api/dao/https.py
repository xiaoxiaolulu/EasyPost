from typing import Any
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
        try:
            tree = Relation.objects.get(project__id=project_id)
            tree = eval(tree.tree)
            return tree
        except (Relation.DoesNotExist, Exception):
            raise Exception("获取目录详情失败")

    @staticmethod
    def get_directory_case(get_queryset, project_id: int):
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
        api = HandelTestData(request.data) # noqa

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
        except (Exception, ):
            raise Exception("解析测试接口失败")

    @classmethod
    def create_or_update_api(cls, request: Any, pk):
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

        try:
            api = HandelTestData(api)
            api_data = api.get_api_template()
            result = run_api(api_data=api_data)
            return result
        except Exception as e:
            raise Exception(f"调试测试接口失败: {e}")

    @staticmethod
    def remove_unwanted_keys(step):
        keys_to_pop = [
            "id", "user", "create_time", "update_time", "directory_id", "priority", "status", "project"
        ]
        for key in keys_to_pop:
            if key in step:
                del step[key]

    @classmethod
    def create_case_step(cls, case_obj, steps):

        for sort, step in enumerate(steps):
            cls.remove_unwanted_keys(step)
            Step.objects.create(
                sort=sort,
                case_id=case_obj,
                **step
            )

    @classmethod
    def create_or_update_case(cls, request, pk=None):
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
        api = HandelTestData(request.data) # noqa

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
        except (Exception, ):
            raise Exception("解析测试用例失败")

    @classmethod
    def run_case_steps(cls, data: dict):

        try:
            runner = HandelTestData()
            steps = data.get('step_data', [])
            name = data.get('name', 'Demo')
            import sys

            case_data = runner.get_case_template(steps, name)
            sys.stdout.write(str(case_data))
            result = run_test(case_data)
            return result
        except Exception as e:
            raise Exception(f"调试测试用例失败: {e}")
