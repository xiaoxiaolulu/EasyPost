from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    viewsets
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.filters.project import ProjectFilter
from api.models.project import Project
from api.schema.project import (
    ProjectSerializers,
    UpdateAvatarSerializers
)
from utils.fatcory import ListAPI


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['name']
    ordering_fields = ['create_time']

    def get_serializer_class(self):
        if self.action == 'update':
            if 'avatar' in self.request.data:
                return UpdateAvatarSerializers
            return ProjectSerializers
        else:
            return ProjectSerializers


class ProjectListViewSet(ListAPI):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['name']
    ordering_fields = ['create_time']
