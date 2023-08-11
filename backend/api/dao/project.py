from api.models.project import (
    Project,
    ProjectRole
)


class ProjectDao:

    @staticmethod
    def project_name_validate(name: str) -> bool:

        try:
            model_object = Project.objects.filter(name=name).first()

            if model_object:
                return True
        except (Project.DoesNotExist, ):
            return False

    @staticmethod
    def create_project_role(validated_data):

        try:
            instance = Project.objects.create(**validated_data)
            ProjectRole.objects.create(project_id=instance.id, user_id=instance.user.id, rode_id=0)
            return instance

        except(Project.DoesNotExist, ProjectRole.DoesNotExist):
            pass
