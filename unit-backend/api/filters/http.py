import django_filters.rest_framework as filters
from api.models.https import ClosedTasks


class ClosedTasksFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='闭环任务模糊查询', lookup_expr='icontains')

    class Meta:
        model = ClosedTasks
        fields = ["name"]
