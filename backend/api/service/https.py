import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import (
    status,
    mixins,
    viewsets
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.dao.https import HttpDao
from api.models.https import (
    Relation,
    Api
)
from api.response.magic import MagicRetrieveApi
from api.schema.https import (
    RelationSerializer,
    ApiSerializer
)
from core.request.http_handler import HttpHandler
from api.response.fatcory import ResponseStandard
from utils.trees import get_tree_max_id


class ApiFastView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

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
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    @staticmethod
    def put(request, **kwargs):
        """
        修改树形结构，ID不能重复
        """
        try:
            body = request.data['body']

            relation = Relation.objects.get(id=kwargs['pk'])
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
            tree = Relation.objects.get(project__id=kwargs['pk'])
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
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def list(self, request, *args, **kwargs):
        context = {
            "request": request,
        }
        serializer = ApiSerializer(data=request.query_params, context=context)
        if serializer.is_valid():
            project = request.query_params.get("project")
            node = int(request.query_params.get("node"))
            name = request.query_params.get("name")

            queryset = HttpDao.list_test_case(node, project, name)
            page = self.paginate_queryset(queryset)  # noqa
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(ResponseStandard.success(serializer.data))
        else:
            return Response(ResponseStandard.failed(data=serializer.errors))


class ApiDetailView(MagicRetrieveApi):

    serializer_class = ApiSerializer
    queryset = Api.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]


class DelApiView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    @staticmethod
    def delete(request, **kwargs):
        try:
            Api.objects.filter(id=kwargs['pk']).delete()
            return Response(ResponseStandard.success())
        except Exception as err:
            return Response(ResponseStandard.failed(data=str(err)))


class SaveOrUpdateApiView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

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
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    @staticmethod
    def post(request, **kwargs):

        try:
            response = HttpDao.run_api_doc(request.data)
            return Response(ResponseStandard.success(data=response))
        except Exception as err:
            return Response(ResponseStandard.failed(msg=str(err)))
