import configparser


class Config:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read('config/genorch.ini')

    def __getattr__(self, name):
        return self.parser[name]

    """
    Provides dict-style access to attributes
    """
    def __getitem__(self, key):
        return getattr(self, key)


"""
Always return an instance of Config
"""
cfg = Config()
