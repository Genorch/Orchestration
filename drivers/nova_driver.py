import json

from novaclient.client import Client


class NovaClient(object):
    def __init__(self):

        with open('../config/os.json') as os_config_file:
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

    def boot_vm(self, image_name, flavor_name, network_label, instance_name):

        image = self.nova.images.find(name=image_name)
        flavor = self.nova.flavors.find(name=flavor_name)
        net = self.nova.networks.find(label=network_label)
        nics = [{'net-id': net.id}]
        instance = self.nova.servers.create(
                name=instance_name, image=image, flavor=flavor, nics=nics)

        print(instance)

    def delete_vm(self, server_name):
            servers_list = self.nova.servers.list()
            server_del = server_name
            server_exists = False

            for server in servers_list:
                if server.name == server_del:
                    print("This server %s exists" % server_del)
                    server_exists = True
                    break

            if not server_exists:
                print("Server %s does not exist" % server_del)
            else:
                print("Deleting server..........")
                self.nova.servers.delete(server)
                print("Server %s deleted" % server_del)
