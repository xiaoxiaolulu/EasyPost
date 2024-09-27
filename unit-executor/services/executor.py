import grpc
from google.protobuf.json_format import MessageToDict
from protos import (
    executor_pb2,
    executor_pb2_grpc
)
from unitrunner.engine.base import (
    run_api,
    run_test
)
from utils.logger import logger
from utils.parser import Parser


class ApiRunServer(executor_pb2_grpc.ExecutorService):

    async def RunApiDoc(self, request:executor_pb2.ApiDocRequest, context):
        try:

            response = run_api(MessageToDict(request))
            responses = executor_pb2.ExecutorResponse()
            Parser.create_report(response, responses)
            return responses
        except Exception as err:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(f'接口调试失败 {str(err)}!')

    async def RunCase(self, request: executor_pb2.CaseRequest, context):
        try:
            response = run_test(MessageToDict(request))
            responses = executor_pb2.ExecutorResponse()
            Parser.create_report(response, responses)
            return responses
        except Exception as err:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(f'接口用例调试失败 {str(err)}!')
