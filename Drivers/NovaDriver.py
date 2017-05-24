import json

from novaclient import client


class NovaClient(object):
    def __init__(self):

        with open('../config/os_example.json') as os_config_file:
                os_cfg = json.load(os_config_file)
                self.nova = client.Client(
                        api_version=os_cfg['OS_COMPUTE_API_VERSION'],
                        username=os_cfg['OS_USERNAME'],
                        password=os_cfg['OS_PASSWORD'],
                        project_id=os_cfg['OS_PROJECT_NAME'],
                        auth_url=os_cfg['OS_AUTH_URL'],
                        region_name=os_cfg['OS_REGION_NAME'])

    def get_vms(self):
        self.nova.servers.list()
