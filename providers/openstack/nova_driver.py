import json

from novaclient.client import Client


class NovaDriver:
    def __init__(self):
        try:
            os_cfg = json.load(open('config/os.json'))

            credentials = {
                "version": os_cfg['OS_COMPUTE_API_VERSION'],
                "auth_url": os_cfg['OS_AUTH_URL'],
                "username": os_cfg['OS_USERNAME'],
                "password": os_cfg['OS_PASSWORD'],
                "project_id": os_cfg['OS_PROJECT_NAME'],
                "region_name": os_cfg['OS_REGION_NAME']
            }

            self.nova = Client(**credentials)
        except FileNotFoundError:
            print("OpenStack configuration not found.")
            exit()

    def get_vms(self):
        return self.nova.servers.list()

    def create_flavor(self, name, ram, hard, vcpu):
        """
        :param name: Descriptive name of the flavor
        :param ram: Memory in MB for the flavor
        :param vcpu: Number of VCPUs for the flavor
        :param hard: Size of local disk in GB
        """
        return self.nova.flavors.create(name, ram, hard, vcpu)

    def find_flavor(self, **args):
        return self.nova.flavors.find(**args)

    def boot_vm(self, image_name, flavor_name, network_labels, instance_name):
        image = self.nova.images.find(name=image_name)
        flavor = self.nova.flavors.find(name=flavor_name)

        nics = []
        for network_label in network_labels:
            net = self.nova.networks.find(label=network_label)
            nics.append({'net-id': net.id})

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
