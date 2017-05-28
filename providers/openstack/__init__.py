from ..base import Provider
from .nova_driver import NovaDriver


class OpenStackProvider(Provider):
    name = 'openstack'

    def __init__(self):
        self.nova_driver = NovaDriver()

    def create_server(self, ram, vcpus, disk):
        # TODO ansible initiation, image name and network configuration
        flavor_id = self.create_flavor()
        self.boot_vm(flavor_id)
