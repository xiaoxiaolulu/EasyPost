import uuid
from abc import ABC
import consul
import requests
import random
from register import base


class ConsulRegister(base.Register, ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.consul = consul.Consul(host=host, port=port)

    def register_consul(
            self,
            name: str,
            address: str,
            port: int,
            tags: str,
            check: dict
    ):

        if check is None:
            check = {
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Timeout": "5s",
                "Interval": "5s",
                "DeregisterCriticalServiceAfter": "15s"
            }
        else:
            check = check

        service_id = uuid.uuid4().hex
        return self.consul.agent.service.register(
            name=name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags,
            check=check
        )

    def deregister(self, service_id):
        return self.consul.agent.service.deregister(service_id)

    def get_all_service(self):
        return self.consul.agent.services()

    def filter_service(self, filter):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter
        }
        return requests.get(url, params=params).json()

    def get_host_port(self, filter):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter
        }
        data = requests.get(url, params=params).json()
        if data:
            service_info = random.choice(list(data.values()))
            return service_info["Address"], service_info["Port"]
        return None, None
