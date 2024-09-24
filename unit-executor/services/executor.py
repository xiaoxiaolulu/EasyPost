import json
from google.protobuf.json_format import MessageToDict
from protos import (
    executor_pb2,
    executor_pb2_grpc
)
from unitrunner.engine.base import run_api
from utils.logger import logger
from utils.parser import Parser


class ApiRunServer(executor_pb2_grpc.ExecutorService):

    def RunApiDoc(self, request, context):
        print(request)
        print(MessageToDict(request))
        response = run_api(MessageToDict(request))
        print(response)
        responses = executor_pb2.ApiDocResponse()
        Parser.create_report(response, responses)
        return responses
