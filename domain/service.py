from service_providers.base import BaseServiceProvider
from utils import common


class Service:
    def __init__(self, provider, targets, opts):
        self.opts = opts

        ips = []
        for vm in targets:
            ips.extend(common.translate_id(vm))

        self.targets = ips
        self.provider = BaseServiceProvider.get(provider)(self.targets)

    def create(self):
        self.provider.create_service(self.opts)
