import json
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    generics
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.project import ProjectDao
from api.emus.ProjectEnum import ProjectRoleEnum
from api.filters.project import ProjectFilter
from api.models.project import (
    Project,
    ProjectRole
)
from api.schema.project import (
    ProjectSerializers,
    ProjectRoleSerializers
)
from api.mixins.magic import (
    MagicDestroyApi,
    MagicUpdateApi,
    MagicCreateApi,
    MagicRetrieveApi,
    ResponseStandard
)


class ProjectListViewSet(generics.ListAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter  # noqa
    search_fields = ['name']
    ordering_fields = ['create_time']

    def list(self, request, *args, **kwargs):

        try:
            queryset = self.filter_queryset(ProjectDao.get_project_list(request.user.id))

            page = self.paginate_queryset(queryset) # noqa
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response(ResponseStandard.success(serializer.data))

        except Exception as err:
            response = ResponseStandard.failed(err)
            return Response(response)


class ProjectDestroyViewSet(MagicDestroyApi):  # noqa
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]


class ProjectUpdateViewSet(MagicUpdateApi):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):
    #     if 'avatar' in self.process.data:
    #         return UpdateAvatarSerializers
    #     return ProjectSerializers


class ProjectCreateViewSet(MagicCreateApi):  # noqa

    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]


class ProjectRetrieveApi(MagicRetrieveApi):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]


class ProjectRoleDestroyViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            response = None
            request_body = json.loads(request.body.decode())
            project_pk = request_body.get("project_id")
            user_pk = request_body.get("user_id")

            has_permission = ProjectDao.check_judge_permission(project_pk, request.user.id)

            if not has_permission:
                response = Response(ResponseStandard.failed(msg=ProjectRoleEnum.DEL_PERMISSION))
            if has_permission:
                instance = ProjectDao.search_user_role(project_pk, user_pk)
                instance.delete()
                response = Response(ResponseStandard.success())
            return response
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class ProjectRoleUpdateViewSet(APIView):
    permission_classes = [IsAuthenticated]  # noqa

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            request_body = json.loads(request.body.decode())
            project_pk = request_body.get("project_id")
            user_pk = request_body.get("user_id")
            roles = request_body.get("roles")

            has_permission = ProjectDao.check_judge_permission(project_pk, request.user.id)
            exist = ProjectDao.check_user_role_exist(project_pk, user_pk)
            if not has_permission:
                return Response(ResponseStandard.failed(msg=ProjectRoleEnum.ADD_PERMISSION))
            if exist:
                return Response(ResponseStandard.failed(msg=ProjectRoleEnum.HAS_PERMISSION))
            else:
                ret = ProjectRole.objects.create(
                    project_id=project_pk,
                    user_id=user_pk,
                    rode_id=roles
                )
                serializer = ProjectRoleSerializers(ret, context={'process': request})
                return Response(ResponseStandard.success(data=serializer.data))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))
