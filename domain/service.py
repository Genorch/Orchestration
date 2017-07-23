from database import db
from tinydb import where
from service_providers.base import BaseServiceProvider


class Service:
    def __init__(self, provider, targets, opts):
        self.opts = opts

        ips = []
        for vm in targets:
            network_interfaces = db.vms.search(where('name') == vm)[0]['ips']
            for nic in network_interfaces:
                ips.append(network_interfaces[nic][0]['addr'])

        self.targets = ips
        self.provider = BaseServiceProvider.get(provider)(self.targets)

    def create(self):
        self.provider.create_service(self.opts)
