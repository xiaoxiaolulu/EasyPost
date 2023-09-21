import json
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.dao.project import ProjectDao
from api.filters.project import ProjectFilter
from api.models.project import (
    Project,
    ProjectRole
)
from api.schema.project import (
    ProjectSerializers,
    ProjectListSerializers, ProjectRoleSerializers
)
from api.response.magic import (
    MagicListAPI,
    MagicDestroyApi,
    MagicUpdateApi,
    MagicCreateApi,
    MagicRetrieveApi,
    ResponseStandard
)


class ProjectListViewSet(MagicListAPI):  # noqa

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter  # noqa
    search_fields = ['name']
    ordering_fields = ['create_time']


class ProjectDestroyViewSet(MagicDestroyApi): # noqa
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]


class ProjectUpdateViewSet(MagicUpdateApi):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    # def get_serializer_class(self):
    #     if 'avatar' in self.request.data:
    #         return UpdateAvatarSerializers
    #     return ProjectSerializers


class ProjectCreateViewSet(MagicCreateApi):  # noqa

    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]


class ProjectRetrieveApi(MagicRetrieveApi):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]


class ProjectRoleDestroyViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            response = None
            request_body = json.loads(request.body.decode())
            project_pk = request_body.get("project_id")
            user_pk = request_body.get("user_id")

            has_permission = ProjectDao.check_judge_permission(project_pk, request.user.id)

            if not has_permission:
                response = Response(ResponseStandard.failed(msg="删除角色失败, 你无改项目权限"))
            if has_permission:
                instance = ProjectDao.search_user_role(project_pk, user_pk)
                instance.delete()
                response = Response(ResponseStandard.success())
            return response
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class ProjectRoleUpdateViewSet(APIView):

    permission_classes = [IsAuthenticated]  # noqa
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

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
                return Response(ResponseStandard.failed(msg="新增角色失败, 你无改项目权限!"))
            if exist:
                return Response(ResponseStandard.failed(msg="当前角色已填权限!"))
            else:
                ret = ProjectRole.objects.create(
                    project_id=project_pk,
                    user_id=user_pk,
                    rode_id=roles
                )
                serializer = ProjectRoleSerializers(ret, context={'request': request})
                return Response(ResponseStandard.success(data=serializer.data))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))
