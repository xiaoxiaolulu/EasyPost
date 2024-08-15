from google.protobuf.json_format import MessageToDict

from protos import executor_pb2, executor_pb2_grpc
from unitrunner.engine.base import run_api
from utils.parser import Parser


class RunServer(executor_pb2_grpc.ExecutorService):

    def RunApiDoc(self, request, context):
        print(MessageToDict(request))

        ret = run_api(MessageToDict(request))

        responses = executor_pb2.ApiDocResponse()
        Parser.create_report(ret, responses)
        print(responses)
        return responses
