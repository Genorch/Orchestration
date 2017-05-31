from ..base import Provider

import json
import os_client_config


class OpenStackProvider(Provider):
    name = 'openstack'

    def __init__(self, region):
        try:
            os_cfg = json.load(open('config/os.json'))

            credentials = {
                "version": os_cfg['OS_COMPUTE_API_VERSION'],
                "auth_url": os_cfg['OS_AUTH_URL'],
                "username": os_cfg['OS_USERNAME'],
                "password": os_cfg['OS_PASSWORD'],
                "project_name": os_cfg['OS_PROJECT_NAME'],
                "region_name": region
            }

            self.nova = os_client_config.make_client('compute', **credentials)
            self.glance = os_client_config.make_client('image', **credentials)
            self.neutron = os_client_config.make_client('network',
                                                        **credentials)
        except FileNotFoundError:
            print("OpenStack configuration not found.")
            exit()

    def create_server(self, image_name, flavor_name, instance_name, networks):
        # TODO ansible initiation, image name and network configuration
        self.nova_driver.boot_vm(
                image_name, flavor_name, networks, instance_name)
