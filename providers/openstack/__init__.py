from ..base import Provider
from .nova_driver import NovaDriver


class OpenStackProvider(Provider):
    name = 'openstack'

    def __init__(self, region):
        self.nova_driver = NovaDriver(region)

    def create_server(self, image_name, flavor_name, instance_name):
        # TODO ansible initiation, image name and network configuration
        self.nova_driver.boot_vm(image_name, flavor_name, [], instance_name)
