import json

from google.protobuf.json_format import MessageToDict
from protos import (
    executor_pb2,
    executor_pb2_grpc
)
from unitrunner.engine.base import run_api
from utils.logger import logger
from utils.parser import Parser


class RunServer(executor_pb2_grpc.ExecutorService):

    def RunApiDoc(self, request, context):
        print(MessageToDict(request))

        response = run_api(MessageToDict(request))
        logger.info(
            f"--------  测试结果 ----------\n"
            f"{json.dumps(response, indent=4, ensure_ascii=False)}\n"
        )
        responses = executor_pb2.ApiDocResponse()
        Parser.create_report(response, responses)
        return responses
