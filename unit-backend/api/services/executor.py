import grpc
from api.services.decorators import grpc_error_handler
from api.services.protos import (
    executor_pb2_grpc,
    executor_pb2
)
from utils.grpconsul import ServiceConsul
from utils.logger import logger
from utils.single import SingletonMeta


servers_consul = ServiceConsul()


class ExecutorStub:
    def __init__(self):
        pass

    @property
    def unit_executor_service_addr(self):
        host, port = servers_consul.fetch_user_service_addresses('unit_executor.services.consul')
        logger.info(f"获取到的地址：{host}:{port}")
        return f"{host}:{port}"

    async def __aenter__(self):
        self.channel = grpc.aio.insecure_channel(self.unit_executor_service_addr)
        stub = executor_pb2_grpc.ExecutorServiceStub(self.channel)
        return stub

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.channel.close()


class UserServiceClient(metaclass=SingletonMeta):

    @grpc_error_handler
    async def run_api_doc(self, api_doc):
        async with ExecutorStub() as stub:
            request = executor_pb2.ApiDocRequest(api_doc)
            response = await stub.RunApiDoc(request)
            return response
