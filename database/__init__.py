from tinydb import TinyDB


class DB:

    def __init__(self):
        self.tinydb = TinyDB('db/db.json')

    def __getattr__(self, item):
        table = self.tinydb.table(item)
        return table


db = DB()
