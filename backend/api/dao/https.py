from api.models.https import Relation, Api
from utils.trees import collections_directory_id, get_relation_tree


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
            raise Exception("获取测试用例失败")

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
            raise Exception("获取测试用例失败")
