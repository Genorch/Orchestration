import configparser


class Config:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read('./ansible.ini')

    def __getattr__(self, name):
        return self.parser['DEFAULT'][name]


"""
Always return an instance of Config
"""
cfg = Config
