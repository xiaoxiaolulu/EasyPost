import django_filters.rest_framework as filters
from api.models.setting import (
    TestEnvironment,
    Address
)


class TestEnvironmentFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按环境名模糊查询', lookup_expr='icontains')

    class Meta:
        model = TestEnvironment
        fields = ["name"]


class AddressFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按地址名称名模糊查询', lookup_expr='icontains')

    class Meta:
        model = Address
        fields = ["name"]
