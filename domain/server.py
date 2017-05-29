from providers.base import BaseProvider


class Server:
    def __init__(self, _id, resources, provider):
        '''
        :param resources: (ram, hard, vcpu)
        '''
        self._id = _id
        self.resources = resources
        self.provider = BaseProvider.get(provider)()

    def create(self):
        self.provider.create_server(*self.resources)
