import socket
import sys
import uuid
import grpc
from typing import Tuple
import settings
from register.consul import ConsulRegister
from services.executor import ApiRunServer
from protos import executor_pb2_grpc
import asyncio
from utils.logger import logger


def get_ip_port() -> Tuple[str, int]:
    sock_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_ip.connect(('8.8.8.8', 80))
    ip = sock_ip.getsockname()[0]
    sock_ip.close()

    sock_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_port.bind(("", 0))
    _, port = sock_port.getsockname()
    sock_port.close()
    return ip, port


async def main():
    ip, port = get_ip_port()
    server = grpc.aio.server()
    executor_pb2_grpc.add_ExecutorServiceServicer_to_server(ApiRunServer(), server)
    server.add_insecure_port(f"{ip}:{port}")

    service_id = str(uuid.uuid1())

    consul = ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    if not consul.register_consul(
            name=settings.SERVICE_NAME,
            service_id=service_id,
            address=ip, port=port,
            tags=settings.SERVICE_TAGS
    ):
        logger.info(f"{settings.SERVICE_NAME} 服务注册失败")

        sys.exit(0)

    await server.start()
    logger.info(f"gRPC服务已经启动：{ip}:{port}")
    try:
        await server.wait_for_termination()
    finally:
        consul.deregister(service_id)


if __name__ == '__main__':
    asyncio.run(main())
