import django_filters.rest_framework as filters
from api.models.report import Main, Detail


class ReportFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按报告名模糊查询', lookup_expr='icontains')

    class Meta:
        model = Main
        fields = ["name"]


class ReportDetailFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按用例名模糊查询', lookup_expr='icontains')

    class Meta:
        model = Detail
        fields = ["name"]
