from typing import Any
from api.models.https import (
    Relation,
    Api
)
from api.models.project import Project
from api.models.setting import Address
from core.request.parser import Format
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
    def get_directory_case(project_id: int):
        try:
            queryset = Api.objects.filter(project__id=project_id).order_by('-update_time')
            return queryset
        except (Api.DoesNotExist, Exception):
            raise Exception("获取测试接口失败")

    @classmethod
    def list_test_case(cls, node: int, project_id: int, name: str = ""):
        try:

            queryset = cls.get_directory_case(project_id)

            if project_id:

                if node == 1:
                    queryset = queryset
                if node != 1:
                    tree = cls.get_directory_tree(project_id)
                    children_tree = get_relation_tree(tree, node)
                    directory_ids = collections_directory_id(children_tree, node)
                    queryset.filter(project__id=project_id, directory_id__in=directory_ids)

                if name:
                    queryset.queryset.filter(name=name)

                return queryset

        except (Api.DoesNotExist, Exception):
            raise Exception("获取测试接口失败")

    @staticmethod
    def add_api_data(api: dict, request: Any):

        api = Format(api) # noqa

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
            'body_type': api.body_type,
            'json': api.json,
            'params': api.params,
            'data': api.data,
            'setup_script': api.setup_script,
            'teardown_script': api.teardown_script,
            'validate': api.validate,
            'extract': api.extract,
            'user': request.user
        }
        try:
            Api.objects.create(**request_body)
        except (Api.DoesNotExist, Exception):
            raise Exception("添加测试接口失败")
