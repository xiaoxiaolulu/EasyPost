from google.protobuf.json_format import MessageToDict
from protos import (
    executor_pb2,
    executor_pb2_grpc
)
from unitrunner.engine.base import (
    run_api,
    run_test
)
from utils.parser import Parser


class ApiRunServer(executor_pb2_grpc.ExecutorService):

    async def RunApiDoc(self, request, context):
        response = run_api(MessageToDict(request))
        responses = executor_pb2.ApiDocResponse()
        Parser.create_report(response, responses)
        return responses
