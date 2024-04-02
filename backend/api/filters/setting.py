import django_filters.rest_framework as filters
from api.models.setting import (
    TestEnvironment,
    Address,
    DataSource
)


class TestEnvironmentFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按环境名模糊查询', lookup_expr='icontains')

    class Meta:
        model = TestEnvironment
        fields = ["name"]


class AddressFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按地址名称模糊查询', lookup_expr='icontains')

    class Meta:
        model = Address
        fields = ["name"]


class DataSourceFilter(filters.FilterSet):

    database = filters.CharFilter(field_name='database', help_text='按数据库名称模糊查询', lookup_expr='icontains')

    class Meta:
        model = DataSource
        fields = ["database"]
