import django_filters.rest_framework as filters
from api.models.plan import Plan


class PlanFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', help_text='按计划名模糊查询', lookup_expr='icontains')

    class Meta:
        model = Plan
        fields = ["name"]
