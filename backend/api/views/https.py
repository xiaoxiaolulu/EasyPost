import json

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.request.http_handler import HttpHandler
from utils.fatcory import ResponseStandard


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
