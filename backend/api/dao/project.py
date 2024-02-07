"""
DESCRIPTION：项目设置数据访问对象
:Created by Null.
"""
from django.db.models import Q
from api.emus.ProjectEnum import ProjectRoleEnum
from api.models.https import Relation
from api.models.project import (
    Project,
    ProjectRole
)
from utils.logger import logger


class ProjectDao:

    @staticmethod
    def get_project_list(user_id):
        """
        查看用户具有权限的项目

        Args:
            user_id: 用户id

        Returns: queryset

        Raises:
            Exception: 查看用户具有权限的项目失败时抛出异常
        """
        try:
            queryset = ProjectRole.objects.filter(user_id=user_id).all()
            queryset = Project.objects.filter(
                Q(id__in=[instance.project_id for instance in queryset]) | Q(private=1) | Q(user_id=user_id))
            return queryset
        except(ProjectRole.DoesNotExist, Exception) as err:
            logger.debug(
                f"🎯获取用户项目列表失败 -> {err}"
            )
            raise Exception("获取用户项目列表失败! ❌")

    @staticmethod
    def project_name_validate(name: str) -> bool:
        """
        验证项目名称

        Args:
            name: 项目名称

        Returns: 布尔值

        Raises:
            Exception: 验证项目名称失败时抛出异常
        """
        try:
            model_object = Project.objects.filter(name=name).first()

            if model_object:
                return True
        except (Project.DoesNotExist,):
            return False

    @staticmethod
    def get_node_template():
        """
        获取树形目录结构数据

        Returns: 数据结构数据
        """

        tree_template = [{  # noqa
            "id": 1,
            "label": "全部",
            "children": []
        }]
        return tree_template

    @classmethod
    def create_project_role(cls, validated_data):
        """
        设置项目权限

        Args:
            validated_data: 项目设置数据

        Returns: Model实例数据

        Raises:
            Exception: 设置项目权限失败时抛出异常
        """

        try:
            instance = Project.objects.create(**validated_data)
            ProjectRole.objects.create(project_id=instance.id, user_id=instance.user.id, rode_id=0)

            template = cls.get_node_template()
            try:
                tree = Relation.objects.get(project=instance)
            except Relation.DoesNotExist:
                for tree_type in range(ProjectRoleEnum.CREATE_RANGE):
                    Relation.objects.create(
                        project=instance,
                        tree=template,
                        type=tree_type
                    )
            return instance

        except(Project.DoesNotExist, ProjectRole.DoesNotExist):
            pass

    @staticmethod
    def check_user_role_exist(project_id, user_id):
        """
        校验用户权限是否存在

        Args:
            project_id: 项目Id
            user_id: 用户Id

        Returns: 布尔值

        Raises:
            Exception: 校验用户权限是否存在失败时抛出异常
        """
        try:
            instance = ProjectRole.objects.filter(Q(project_id=project_id) & Q(user_id=user_id)).first()

            if instance is not None:
                return True
        except(ProjectRole.DoesNotExist, Exception):
            return False

    @staticmethod
    def check_judge_permission(project_id, user_id):
        """
        校验用户项目权限

        Args:
            project_id: 项目Id
            user_id: 用户Id

        Returns: 布尔值

        Raises:
            Exception: 校验用户项目权限失败时抛出异常
        """
        try:
            instance = Project.objects.get(pk=project_id)
            owner = instance.user.id
            permission = False if owner != user_id else True

            return permission
        except(Project.DoesNotExist, Exception) as err:
            logger.debug(
                f"🎯项目未找到 -> {err}"
            )
            raise Exception("项目未找到 ❌")

    @staticmethod
    def search_user_role(project_id, user_id):
        """
        搜索用户项目权限

        Args:
            project_id: 项目Id
            user_id: 用户Id

        Returns: 项目权限数据

        Raises:
            Exception: 搜索用户项目权限失败时抛出异常
        """
        try:
            instance = ProjectRole.objects.filter(Q(project_id=project_id) & Q(user_id=user_id))
            return instance
        except(ProjectRole.DoesNotExist, Exception) as err:
            logger.debug(
                f"🎯该项目未找到该角色权限！ -> {err}"
            )
            raise Exception("该项目未找到该角色权限！❌")
