import django_filters.rest_framework as filters
from api.models.project import Project


class ProjectFilter(filters.FilterSet):

    id = filters.CharFilter(field_name='id', help_text='按项目ID查询', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', help_text='按项目名模糊查询', lookup_expr='icontains')
    created_gt = filters.DateTimeFilter(field_name='create_time', help_text='按创建时间gt查询', lookup_expr='gt')
    created_lt = filters.DateTimeFilter(field_name='create_time', help_text='按创建时间lt查询', lookup_expr='lt')

    class Meta:
        model = Project
        fields = ["id", "name", "created_gt", "created_lt"]
