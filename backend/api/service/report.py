from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    mixins,
    status,
    viewsets
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.dao.report import ReportDao
from api.filters.report import (
    ReportFilter
)
from api.mixins.magic import (
    MagicListAPI
)
from api.models.report import (
    Main,
    Detail
)
from api.schema.report import (
    ReportMainSerializer,
    ReportDetailSerializers,
)


class ReportDetailView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = ReportDetailSerializers
    queryset = Detail.objects
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        context = {
            "request": request,
        }
        serializer = ReportDetailSerializers(data=request.query_params, context=context)
        if serializer.is_valid():
            report_id = request.query_params.get("id")
            name = request.query_params.get("name")

            queryset = self.get_queryset()
            queryset = ReportDao.detail_step_list(queryset, report_id, name)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportListViewSet(MagicListAPI):

    queryset = Main.objects.all()
    serializer_class = ReportMainSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReportFilter
    search_fields = ['name']
    ordering_fields = ['create_time']
