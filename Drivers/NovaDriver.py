import json

from novaclient.client import Client


class NovaClient(object):
    def __init__(self):

        with open('../config/os_example.json') as os_config_file:
                os_cfg = json.load(os_config_file)

                credentials = {
                        "version": os_cfg['OS_COMPUTE_API_VERSION'],
                        "auth_url": os_cfg['OS_AUTH_URL'],
                        "username": os_cfg['OS_USERNAME'],
                        "api_key": os_cfg['OS_PASSWORD'],
                        "project_id": os_cfg['OS_PROJECT_NAME'],
                        "region_name": os_cfg['OS_REGION_NAME']
                        }

                self.nova = Client(**credentials)

    def get_vms(self):
        print(self.nova.servers.list())
