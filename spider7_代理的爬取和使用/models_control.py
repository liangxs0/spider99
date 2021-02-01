from models import *
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

Table = {
    "proxies":Proxy,
}

class MysqlServer(object):
    def __init__(self):
        pass

    def get_info(self):
        pass

    def update_info(self):
        pass

    def find_info(self):
        pass

    def delete_info(self):
        pass

    def __del__(self):
        pass