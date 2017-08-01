from service_providers.base import BaseServiceProvider


class Service:
    def __init__(self, provider, targets, opts):
        self.opts = opts
        self.targets = targets
        self.provider = BaseServiceProvider.get(provider)(self.targets)

    def create(self):
        self.provider.create_service(self.opts)
