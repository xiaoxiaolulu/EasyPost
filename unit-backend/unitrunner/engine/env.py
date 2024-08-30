import requests
from unitrunner.database.DBClient import DBClient


class BaseEnv(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __getattr__(self, item):
        return super().__getitem__(item)


ENV = BaseEnv()
db = DBClient()
DEBUG = True
session = requests.Session()
