from service_providers.ansible_driver import Ansible


class Service:
    def __init__(self, name, targets, provider):
        self.name = name
        self.targets = targets
        self.provider = Ansible()

    def create(self):
        self.provider.create_service(self.name, self.targets)
