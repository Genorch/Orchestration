from providers.base import BaseProvider


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
        # TODO ansible initiation
        self._id = self.provider.create_server(
            self.image, self.flavor, self.name, self.networks)

    @property
    def ips(self):
        print(self.provider.ips(self._id))
