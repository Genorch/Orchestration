from providers.base import BaseProvider
from database import db


class Server:
    def __init__(self, name, image, flavor, region, provider, networks, key=None):
        self._id = None
        self.name = name
        self.flavor = flavor
        self.region = region
        self.image = image
        self.networks = networks
        self.key = key
        self.provider = BaseProvider.get(provider)(region)

    @staticmethod
    def truncate():
        vms = db.vms.all()
        for vm in vms:
            provider = BaseProvider.get(vm['provider'])(vm['region'])
            provider.delete_server(vm['_id'])
            db.vms.remove(eids=[vm.eid])

    def create(self):
        self._id = self.provider.create_server(
            self.image, self.flavor, self.name, self.networks, self.key)

        while self.ips == {}: pass

        # Store the created VM inside database
        vm_data = {
            "_id": self._id,
            "name": self.name,
            "flavor": self.flavor,
            "region": self.region,
            "image": self.image,
            "networks": self.networks,
            "ips": self.ips,
            "provider": self.provider.name
            }

        if self.key is not None:
            vm_data['key'] = self.key

        db.vms.insert(vm_data)

    def delete(self):
        self.provider.delete_server(self._id)

    @property
    def ips(self):
        return self.provider.ips(self._id)
