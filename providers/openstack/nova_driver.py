import json

from novaclient.client import Client


class NovaDriver:
    def __init__(self):
        try:
            os_cfg = json.load(open('../config/os.json'))

            credentials = {
                "version": os_cfg['OS_COMPUTE_API_VERSION'],
                "auth_url": os_cfg['OS_AUTH_URL'],
                "username": os_cfg['OS_USERNAME'],
                "api_key": os_cfg['OS_PASSWORD'],
                "project_id": os_cfg['OS_PROJECT_NAME'],
                "region_name": os_cfg['OS_REGION_NAME']
            }

            self.nova = Client(**credentials)
        except FileNotFoundError:
            print("OpenStack configuration not found.")
            exit()

    def get_vms(self):
        return self.nova.servers.list()

    def create_flavor(self, name, ram, vcpus, disk):
        """
        :param name: Descriptive name of the flavor
        :param ram: Memory in MB for the flavor
        :param vcpus: Number of VCPUs for the flavor
        :param disk: Size of local disk in GB
        """
        self.nova.flavors.create(name, ram, vcpus, disk)

    def boot_vm(self, image_name, flavor_name, network_label, instance_name):
        image = self.nova.images.find(name=image_name)
        flavor = self.nova.flavors.find(name=flavor_name)
        net = self.nova.networks.find(label=network_label)
        nics = [{'net-id': net.id}]
        instance = self.nova.servers.create(
                name=instance_name, image=image, flavor=flavor, nics=nics)

        return instance

    def delete_vm(self, server_name):
            servers_list = self.nova.servers.list()
            server_del = server_name

            for server in servers_list:
                if server.name == server_del:
                    print("This server %s exists" % server_del)
                    break
            else:
                print("Server %s does not exist" % server_del)

            print("Deleting server..........")
            self.nova.servers.delete(server)
            print("Server %s deleted" % server_del)
