from ..providers.base import BaseProvider


class Server:
    def __init__(self, provider):
        self.provider = BaseProvider.get(provider)
