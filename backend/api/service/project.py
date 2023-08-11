from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.filters.project import ProjectFilter
from api.models.project import Project
from api.schema.project import (
    ProjectSerializers,
    UpdateAvatarSerializers,
    ProjectListSerializers
)
from api.response.fatcory import (
    MagicListAPI,
    MagicDestroyApi,
    MagicUpdateApi,
    MagicCreateApi,
    MagicRetrieveApi
)


class ProjectListViewSet(MagicListAPI):

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['name']
    ordering_fields = ['create_time']


class ProjectDestroyViewSet(MagicDestroyApi):

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
