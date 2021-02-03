from models import *
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from m_log import *
import time

Table = {
    "proxies":Proxy,
}

class MysqlServer(object):
    def __init__(self, DBsession):
        self.DBsession = DBsession

    def get_info(self):
        pass

    @log_exception
    def insert_info(self, ip, port, type):
        session = self.DBsession()
        ids = session.query(Table["proxies"]).filter_by(ip=ip).all()

        if len(ids) != 0:
            logging.info(f"{ip}-{port}-{type}-重复")
            return None
        insert_da_tag = Table["proxies"](
            ip=ip, port=port, type=type,
            uptime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        session.add(insert_da_tag)
        session.commit()
        logging.info(f"{ip}-{port}-{type}-入库")
        session.close()
        return True

    def update_info(self):
        pass

    def find_info(self):
        pass

    def delete_info(self):
        pass

    def __del__(self):
        pass