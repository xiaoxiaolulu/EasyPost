import json
from google.protobuf.json_format import MessageToDict
from protos import (
    executor_pb2,
    executor_pb2_grpc
)
from unitrunner.engine.base import run_api
from unitrunner.request.parser import HandelTestData
from utils.logger import logger
from utils.parser import Parser


class ApiRunServer(executor_pb2_grpc.ExecutorService):

    def RunApiDoc(self, request, context):
        parser = HandelTestData(MessageToDict(request))
        api_doc = parser.get_api_template()
        response = run_api(api_doc)
        print(json.dumps(dict(response), ensure_ascii=False, indent=2))
        responses = executor_pb2.ApiDocResponse()
        Parser.create_report(response, responses)

        return responses
