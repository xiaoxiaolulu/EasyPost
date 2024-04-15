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
        Retrieves a list of projects for the specified user.

        Args:
            user_id: The ID of the user to get projects for.

        Returns:
            A queryset of projects for the user.

        Raises:
            Exception: If an error occurs while retrieving the projects.
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
        Checks if a project name already exists in the database.

        Args:
            name: The project name to validate.

        Returns:
            True if the name already exists, False otherwise.
        """
        try:
            model_object = Project.objects.filter(name=name).first()

            if model_object:
                return True
        except (Project.DoesNotExist,):
            return False

    @staticmethod
    def project_same_validate(name: str) -> bool:
        """
        Checks if a project name already exists in the database.

        Args:
            name: The project name to validate.

        Returns:
            True if the name already exists, False otherwise.
        """
        try:
            model_object = Project.objects.filter(name=name).count()

            if model_object > 1:
                return True
        except (Project.DoesNotExist,):
            return False

    @staticmethod
    def get_node_template():
        """
        Generates a default tree template for the node list.

        Returns:
            A list representing the tree template.
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
        Creates a new project, project role, and optional tree relations.

        Args:
            validated_data: A dictionary containing validated project data.

        Returns:
            The created Project instance on success.

        Raises:
          - Implicitly raises exceptions from model creation methods if unsuccessful.
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
        Checks if a user has a role associated with a specific project.

        Args:
            project_id: The ID of the project.
            user_id: The ID of the user.

        Returns:
            True if the user has a role for the project, False otherwise.
        """
        try:
            instance = ProjectRole.objects.filter(Q(project_id=project_id) & Q(user_id=user_id)).first()

            if instance is not None:
                return True
        except (ProjectRole.DoesNotExist, Exception):
            return False

    @staticmethod
    def check_judge_permission(project_id, user_id):
        """
        Checks if the user has permission to judge submissions for a given project.

        Args:
            project_id: The ID of the project.
            user_id: The ID of the user.

        Returns:
            True if the user has permission to judge, False otherwise.

        Raises:
            Exception: If the project does not exist.
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
        Retrieves the project role for a specific user in a given project.

        Args:
            project_id: The ID of the project.
            user_id: The ID of the user.

        Returns:
            A queryset containing the ProjectRole object for the user, if it exists.

        Raises:
            Exception: If an error occurs while retrieving the role.
        """

        try:
            instance = ProjectRole.objects.filter(Q(project_id=project_id) & Q(user_id=user_id))
            return instance
        except(ProjectRole.DoesNotExist, Exception) as err:
            logger.debug(
                f"🎯该项目未找到该角色权限！ -> {err}"
            )
            raise Exception("该项目未找到该角色权限！❌")
