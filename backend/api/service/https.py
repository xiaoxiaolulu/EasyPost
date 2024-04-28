import json
import os
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import (
    status,
    mixins,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.dao.https import HttpDao
from api.mixins.async_generics import AsyncAPIView
from api.models.https import (
    Relation,
    Api,
    Case
)
from api.mixins.magic import (
    MagicRetrieveApi
)
from api.schema.https import (
    RelationSerializer,
    ApiSerializer,
    CaseSerializers
)
from config.settings import MEDIA_ROOT
from unitrunner.request.http_handler import HttpHandler
from api.response.fatcory import ResponseStandard
from utils.api_migrate import (
    DataMigrator,
    SwaggerDataSource,
    UitRunnerSource,
    PostManDataSource
)
from utils.trees import (
    get_tree_max_id
)


class ApiFastView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            request_body = json.loads(request.body.decode())
            client = HttpHandler(request_body=request_body)
            response = client.request()
            if response.get("status"):
                return Response(ResponseStandard.success(data=response))
            return Response(ResponseStandard.failed(response.get("msg"), data=response))
        except Exception as err:
            return Response(ResponseStandard.failed(err))


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
            "request": request,
        }
        serializer = ApiSerializer(data=request.query_params, context=context)
        if serializer.is_valid():  # noqa
            project = request.query_params.get("project")
            node = request.query_params.get("node")
            name = request.query_params.get("name")

            # queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')

            # tree = Relation.objects.get(project__id=project)
            # tree = eval(tree.tree)
            #
            # if node == 1:
            #     queryset = queryset
            #
            # else:
            #     children_tree = get_relation_tree(tree, node)
            #     directory_ids = collections_directory_id(children_tree, node)
            #     queryset = queryset.filter(project__id=project, directory_id__in=directory_ids)
            #
            # if name:
            #     queryset = queryset.filter(name=name)
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
            response = HttpDao.create_or_update_api(request, pk=kwargs['pk'])
            return Response(ResponseStandard.success(
                data={"api_id": response}
            ))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))


class RunApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = HttpDao.run_api_doc(request.data)
            return Response(ResponseStandard.success(data=response))
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


class RunCaseView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = HttpDao.run_case_steps(request.data)
            return Response(ResponseStandard.success(data=response))
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
            if import_type:
                import_mapping = {
                    "swagger": SwaggerDataSource(),
                    "postman": PostManDataSource()
                }
                migrator = DataMigrator(import_mapping.get(import_type), UitRunnerSource())
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
            "request": request,
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
