from service_providers.ansible_driver import Ansible
from database import db
from tinydb import where


class Service:
    def __init__(self, name, targets):
        self.name = name

        ips = []
        for vm in targets:
            network_interfaces = db.vms.search(where('name') == vm)[0]['ips']
            print(network_interfaces)
            for nic in network_interfaces:
                ips.append(network_interfaces[nic][0]['addr'])

        self.targets = ips
        self.provider = Ansible(self.targets)

    def create(self):
        self.provider.create_service(self.name)
