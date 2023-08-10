from api.models.project import Project


class ProjectDao:

    @staticmethod
    def project_name_validate(name: str) -> bool:

        try:
            model_object = Project.objects.filter(name=name).first()

            if model_object:
                return True
        except (Project.DoesNotExist, ):
            return False
