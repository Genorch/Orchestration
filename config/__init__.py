import configparser


class Config:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read('config/ansible.ini')
        self.config = self.parser['DEFAULT']

    def __getattr__(self, name):
       return self.config[name]


"""
Always return an instance of Config
"""
cfg = Config()
