import grpc
from services.executor import RunServer
from protos import executor_pb2_grpc
import asyncio
from utils.logger import logger


async def main():
    server = grpc.aio.server()
    executor_pb2_grpc.add_ExecutorServiceServicer_to_server(RunServer(), server)
    server.add_insecure_port("0.0.0.0:5001")
    await server.start()
    logger.info("启动服务: 0.0.0.0:5001")
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(main())
