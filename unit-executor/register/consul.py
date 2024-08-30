import consul


class ConsulRegister(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.consul = consul.Consul(host=host, port=port)

    def register_consul(
            self,
            name,
            service_id,
            address,
            port,
            tags
    ):

        register = self.consul.agent.service.register(
            name=name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags,
            check=consul.Check.tcp(host=address, port=port, interval='10s')
        )
        return register

    def deregister(self, service_id):
        return self.consul.agent.service.deregister(service_id)
