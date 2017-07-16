from service_providers.ansible_driver import Ansible
from database import db
from tinydb import where


class Service:
    def __init__(self, name, targets, provider=Ansible()):
        self.name = name

        ips = []
        for vm in targets:
            network_intefaces = db.vms.search(where('name') == vm)[0]['ips']
            print(network_intefaces)
            for nic in network_intefaces:
                ips.append(network_intefaces[nic][0]['addr'])

        self.targets = ips
        self.provider = provider

    def create(self):
        self.provider.create_service(self.name, self.targets)
