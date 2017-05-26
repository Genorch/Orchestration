from providers.base import BaseProvider
from ansible import AnsibleDriver


class Server:
    def __init__(self, _id, _class, provider):
        self._id = _id
        self._class = _class
        self.provider = BaseProvider.get(provider)()

    def create_vm(self):
        self.provider.create_server()
        AnsibleDriver(self._class).setup
