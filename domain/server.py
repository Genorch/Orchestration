from providers.base import BaseProvider
from database import db


class Server:
    def __init__(self, _id, image, flavor, region, provider, networks):
        self._id = None
        self.name = _id
        self.flavor = flavor
        self.region = region
        self.image = image
        self.networks = networks
        self.provider = BaseProvider.get(provider)(region)

    def create(self):
        self._id = self.provider.create_server(
            self.image, self.flavor, self.name, self.networks)
        db.vms.insert({
            "name": self.name,
            "flavor": self.flavor,
            "region": self.region,
            "image": self.image,
            "networks": self.networks,
            "ips": self.ips})

    @property
    def ips(self):
        return self.provider.ips(self._id)
