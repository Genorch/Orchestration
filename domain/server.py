from providers.base import BaseProvider


class Server:
    def __init__(self, _id, image, flavor, region, provider):
        self._id = _id
        self.flavor = flavor
        self.region = region
        self.image = image
        self.provider = BaseProvider.get(provider)(region)

    def create(self):
        self.provider.create_server(self.image, self.flavor, self._id)
