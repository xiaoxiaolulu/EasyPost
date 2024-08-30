import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")


# consul的配置
CONSUL_HOST = "127.0.0.1"
CONSUL_PORT = "8500"

# 服务相关的配置
SERVICE_NAME = "unit_executor"
SERVICE_TAGS = ['unit_executor', 'grpc']
