import django_filters.rest_framework as filters
from api.models.setting import (
    TestEnvironment,
    DataSource,
    Functions,
    Notice
)


class TestEnvironmentFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按环境名模糊查询', lookup_expr='icontains')

    class Meta:
        model = TestEnvironment
        fields = ["name"]


class DataSourceFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='database', help_text='按数据库名称模糊查询', lookup_expr='icontains')

    class Meta:
        model = DataSource
        fields = ["database"]


class FunctionsFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按函数名称模糊查询', lookup_expr='icontains')

    class Meta:
        model = Functions
        fields = ["name"]


class NoticeFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按函数名称模糊查询', lookup_expr='icontains')

    class Meta:
        model = Notice
        fields = ["name"]
