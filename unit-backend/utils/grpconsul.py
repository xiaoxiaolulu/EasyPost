import random
import socket
from dns import resolver
from config import settings


class ServiceConsul(object):

    def __init__(self):
        self.consul_host = settings.CONSUL_HOST
        self.consul_dns_port = settings.CONSUL_DNS_PORT

    @staticmethod
    def extract_ip_prefix(encoded_address: str):
        match = encoded_address.split(".")[0]
        return match

    def decode_address(self, encoded_address):
        hex_address = self.extract_ip_prefix(encoded_address)
        binary_address = bytes.fromhex(hex_address)
        return socket.inet_ntoa(binary_address)

    def fetch_user_service_addresses(self, srv_record_name):
        custom_resolver = resolver.Resolver()
        custom_resolver.nameservers = [self.consul_host]
        custom_resolver.port = self.consul_dns_port

        try:
            answer = custom_resolver.resolve(srv_record_name, 'SRV')
            selected_rdata = random.choice(answer)
            ip_address = self.decode_address(selected_rdata.target.to_text())
            return ip_address, selected_rdata.port
        except resolver.NoAnswer as e:
            print(f"No answer found for the query: {srv_record_name}")
        except resolver.NXDOMAIN as e:
            print(f"Domain not found: {srv_record_name}")
        except Exception as e:
            print(f"Error occurred while resolving DNS: {str(e)}")


def main():
    srv_record_name = 'unit_executor.service.consul'
    cons = ServiceConsul()
    address, port = cons.fetch_user_service_addresses(srv_record_name)
    print(address, port)


if __name__ == "__main__":
    main()
