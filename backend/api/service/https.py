import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.models.https import Relation
from api.schema.https import RelationSerializer
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
    def patch(request, **kwargs):
        """
        修改树形结构，ID不能重复
        """
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
        return Response(serializer)

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
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer)
