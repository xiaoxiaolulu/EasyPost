import django_filters.rest_framework as filters
from api.models.report import Main


class ReportFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按报告名模糊查询', lookup_expr='icontains')

    class Meta:
        model = Main
        fields = ["name"]
