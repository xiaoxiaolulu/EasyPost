from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from api.filters.report import ReportFilter
from api.mixins.magic import (
    MagicRetrieveApi,
    MagicListAPI
)
from api.models.report import (
    Main,
    Detail
)
from api.schema.report import (
    ReportMainSerializer,
    ReportDetailSerializers
)


class ReportDetailView(MagicRetrieveApi):
    serializer_class = ReportDetailSerializers
    queryset = Detail.objects.all()
    permission_classes = [IsAuthenticated]


class ReportListViewSet(MagicListAPI):

    queryset = Main.objects.all()
    serializer_class = ReportMainSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReportFilter
    search_fields = ['name']
    ordering_fields = ['create_time']
