import os
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from google.protobuf.json_format import MessageToDict
from rest_framework import filters
from rest_framework import (
    status,
    mixins,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.https import HttpDao
from api.events.registry import registry
from api.filters.http import ClosedTasksFilter
from api.mixins.async_generics import AsyncAPIView
from api.models import https
from api.models.https import (
    Relation,
    Api,
    Case,
    ClosedTasks,
    Step
)
from api.mixins.magic import (
    MagicRetrieveApi,
    MagicListAPI
)
from api.schema.https import (
    RelationSerializer,
    ApiSerializer,
    CaseSerializers,
    ClosedTasksSerializers,
    CaseStepSerializers
)
from config.settings import MEDIA_ROOT
from api.response.fatcory import ResponseStandard
from utils.api_migrate import (
    DataMigrator,
    UitRunnerSource
)
from utils.trees import (
    get_tree_max_id
)


class TreeView(APIView):
    serializer_class = RelationSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request, **kwargs):
        """
        修改树形结构，ID不能重复
        """
        try:
            body = request.data['body']
            relation = Relation.objects.get(id=kwargs['pk'], type=kwargs['use_type'])
            relation.tree = body
            relation.save()

            node = relation.tree

            serializer = {
                "tree": node,
                "id": relation.id,
                "maxId": get_tree_max_id(node),
                "success": status.HTTP_200_OK
            }
            return Response(ResponseStandard.success(data=serializer))
        except ObjectDoesNotExist:
            Response(ResponseStandard.failed())

    @staticmethod
    def get(request, **kwargs):
        try:
            tree = Relation.objects.get(project__id=kwargs['pk'], type=kwargs['use_type'])
            node = eval(tree.tree)
            serializer = {
                "tree": node,
                "id": tree.id,
                "maxId": get_tree_max_id(node),
                "success": status.HTTP_200_OK
            }
        except ObjectDoesNotExist:
            return Response(ResponseStandard.failed())

        return Response(ResponseStandard.success(data=serializer))


class ApiTestListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ApiSerializer
    queryset = Api.objects
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        context = {
            "process": request,
        }
        serializer = ApiSerializer(data=request.query_params, context=context)
        if serializer.is_valid():  # noqa
            project = request.query_params.get("project")
            node = request.query_params.get("node")
            name = request.query_params.get("name")

            queryset = self.get_queryset()
            queryset = HttpDao.list_test_case(queryset, node, project, name)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDetailView(MagicRetrieveApi):
    serializer_class = ApiSerializer
    queryset = Api.objects.all()
    permission_classes = [IsAuthenticated]


class DelApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, **kwargs):
        try:
            Api.objects.filter(id=kwargs['pk']).delete()
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(data=str(err)))


class SaveOrUpdateApiView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = HttpDao.create_or_update_api(request, pk=kwargs['pk'], models=https.Api)
            return Response(ResponseStandard.success(
                data={"api_id": response}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class RunApiView(AsyncAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    async def post(request, **kwargs):

        try:
            response = await HttpDao.run_api_doc(request.data)
            return Response(ResponseStandard.success(data=MessageToDict(response)))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class SaveOrUpdateCaseView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = HttpDao.create_or_update_case(request, pk=kwargs['pk'])
            return Response(ResponseStandard.success(
                data={"case_id": response}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class DelCaseView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, **kwargs):
        try:
            HttpDao.delete_case(pk=kwargs['pk'])
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(data=str(err)))


class CaseDetailView(MagicRetrieveApi):
    serializer_class = CaseSerializers
    queryset = Case.objects.all()
    permission_classes = [IsAuthenticated]


class CaseStepDetailView(MagicRetrieveApi):

    serializer_class = CaseStepSerializers
    queryset = Step.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(pk=self.kwargs['pk'])
        except Step.DoesNotExist:
            obj = Api.objects.get(pk=self.kwargs['pk'])
        return obj


class SaveOrUpdateStepView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = HttpDao.create_or_update_api(request, pk=kwargs['pk'], models=https.Step)
            return Response(ResponseStandard.success(
                data={"api_id": response}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class RunCaseView(AsyncAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    async def post(request, **kwargs):

        try:
            response = await HttpDao.run_case_steps(request.data)
            return Response(ResponseStandard.success(data=MessageToDict(response)))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class ImportApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):

        try:
            files = request.FILES.get('file')
            filepath = os.path.join(MEDIA_ROOT, files.name)

            with open(filepath, 'wb+') as f:
                for chunk in files.chunks():
                    f.write(chunk)

            import_type = request.data.get("type", "swagger")
            migrator = DataMigrator(registry.get(import_type), UitRunnerSource())
            migrator.migrate(filename=filepath, request=request, pk=kwargs["pk"], type=import_type)
            return Response(ResponseStandard.success())

        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class ApiSnapshotView(AsyncAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    async def post(request, **kwargs):

        try:
            await HttpDao.create_api_snapshot(request)
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class CaseListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CaseSerializers
    queryset = Case.objects
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        context = {
            "process": request,
        }
        serializer = CaseSerializers(data=request.query_params, context=context)

        if serializer.is_valid():  # noqa
            project = request.query_params.get("project")
            node = request.query_params.get("node")
            name = request.query_params.get("name")

            queryset = self.get_queryset()
            queryset = HttpDao.list_test_case(queryset, node, project, name)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClosedTasksViewSet(MagicListAPI):

    queryset = ClosedTasks.objects.all()
    serializer_class = ClosedTasksSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ClosedTasksFilter
    search_fields = ['name']
    ordering_fields = ['create_time']


class ClosedTasksRetrieveApi(MagicRetrieveApi):

    queryset = ClosedTasks.objects.all()
    serializer_class = ClosedTasksSerializers
    permission_classes = [IsAuthenticated]
