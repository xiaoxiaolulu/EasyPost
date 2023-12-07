from typing import Any
from api.models.https import (
    Relation,
    Api
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
    def list_test_case(cls, get_queryset, node: int, project_id: int, name: str = ""):
        try:
            queryset = cls.get_directory_case(get_queryset, project_id)
            tree = cls.get_directory_tree(project_id)

            if project_id:
                if node == 1:
                    queryset = queryset
                else:
                    children_tree = get_relation_tree(tree, node)
                    directory_ids = collections_directory_id(children_tree, node)
                    queryset = queryset.filter(project__id=project_id, directory_id__in=directory_ids)

                if name:
                    queryset = queryset.filter(name=name)

                return queryset

        except (Api.DoesNotExist, Exception):
            raise Exception("获取测试接口失败")

    @staticmethod
    def parser_api_data(request: Any):

        api = HandelTestData(request.data) # noqa

        request_body = {
            'name': api.name,
            'project': Project.objects.get(id=api.project),
            'directory_id': api.directory_id,
            'method': api.method,
            'url': api.url,
            'tags': api.tags,
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
            request_body = cls.parser_api_data(request)
            if pk:
                update_obj = Api.objects.filter(id=pk)
                update_obj.update(**request_body)
                update_pk = pk
            else:
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
