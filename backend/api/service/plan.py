from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.https import HttpDao
from api.dao.plan import PlanDao
from api.filters.plan import PlanFilter
from api.mixins.async_generics import AsyncAPIView
from api.mixins.magic import (
    MagicRetrieveApi,
    MagicListAPI
)
from api.models.plan import Plan
from api.response.fatcory import ResponseStandard
from api.schema.plan import PlanSerializers


class SavePlanView(AsyncAPIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    async def post(request, **kwargs):

        try:
            await PlanDao.create_plan(request)
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class UpdatePlanView(AsyncAPIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    async def post(request, **kwargs):

        try:
            await PlanDao.update_plan(request, pk=kwargs['pk'])
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class UpdatePlanStateView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, task_id, target_status):
        try:
            response = PlanDao.update_test_plan_state(task_id, target_status)

            return Response(ResponseStandard.success(
                data=response
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class RunPlanView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            case_list = request.data.get('case_list', [])
            response = HttpDao.run_test_suite(case_list)
            return Response(ResponseStandard.success(data=response))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class DelPlanView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, **kwargs):
        try:
            Plan.objects.filter(id=kwargs['pk']).delete()
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(data=str(err)))


class PlanDetailView(MagicRetrieveApi):
    serializer_class = PlanSerializers
    queryset = Plan.objects.all()
    permission_classes = [IsAuthenticated]


class PlanListViewSet(MagicListAPI):

    queryset = Plan.objects.all()
    serializer_class = PlanSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PlanFilter # noqa
    search_fields = ['name']
    ordering_fields = ['create_time']
