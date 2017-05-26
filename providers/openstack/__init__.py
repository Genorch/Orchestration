from ..base import Provider
from .nova_driver import NovaDriver


class OpenStackProvider(Provider):
    name = 'openstack'

    def __init__(self):
        self.nova_driver = NovaDriver()

    def create_server(self):
        print(self.get_vms())
        pass
