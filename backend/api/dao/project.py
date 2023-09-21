from django.db.models import Q
from api.models.https import Relation
from api.models.project import (
    Project,
    ProjectRole
)


class ProjectDao:

    @staticmethod
    def get_project_list(user_id):
        """
        查看用户具有权限的项目
        """
        try:
            queryset = ProjectRole.objects.filter(user_id=user_id).all()
            queryset = Project.objects.filter(
                Q(id__in=[instance.project_id for instance in queryset]) | Q(private=1) | Q(user_id=user_id))
            return queryset
        except(ProjectRole.DoesNotExist, Exception):
            raise Exception("获取用户项目列表失败!")

    @staticmethod
    def project_name_validate(name: str) -> bool:

        try:
            model_object = Project.objects.filter(name=name).first()

            if model_object:
                return True
        except (Project.DoesNotExist,):
            return False

    @staticmethod
    def create_project_role(validated_data):

        try:
            instance = Project.objects.create(**validated_data)
            ProjectRole.objects.create(project_id=instance.id, user_id=instance.user.id, rode_id=0)

            tree_template = [{  # noqa
                "id": 1,
                "label": "全部",
                "nodeTier": 1,
                "children": [],
                "parent": 0
            }]

            try:
                tree = Relation.objects.get(project=instance)
            except Relation.DoesNotExist:
                Relation.objects.create(
                    project=instance,
                    tree=tree_template
                )
            return instance

        except(Project.DoesNotExist, ProjectRole.DoesNotExist):
            pass

    @staticmethod
    def check_user_role_exist(project_id, user_id):
        try:
            instance = ProjectRole.objects.filter(Q(project_id=project_id) & Q(user_id=user_id)).first()

            if instance is not None:
                return True
        except(ProjectRole.DoesNotExist, Exception):
            return False

    @staticmethod
    def check_judge_permission(project_id, user_id):
        try:
            instance = Project.objects.get(pk=project_id)
            owner = instance.user.id
            permission = False if owner != user_id else True

            return permission
        except(Project.DoesNotExist, Exception):

            raise Exception("项目未找到")

    @staticmethod
    def search_user_role(project_id, user_id):
        try:
            instance = ProjectRole.objects.filter(Q(project_id=project_id) & Q(user_id=user_id))
            return instance
        except(ProjectRole.DoesNotExist, Exception):
            raise Exception("该项目未找到该角色权限！")
