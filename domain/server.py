from providers.base import BaseProvider


class Server:
    def __init__(self, _id, _class, provider):
        self._id = _id
        self._class = _class
        self.provider = BaseProvider.get(provider)
