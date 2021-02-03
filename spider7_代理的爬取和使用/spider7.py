'''
2021-1-29 昆山 晴
天行健，君子以自強不息，地勢坤，君子以厚德载物。
自己做个代理池，爬取几个代理网站然后将hhtp和https的分别放到，mysql中
'''

from spider_base import my_requests
from pyquery import PyQuery
import asyncio
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import random
import time

from settings import *
from m_log import *
from models_control import MysqlServer

#请求头
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

class KuaiProxies:
    '''
    爬取快代理
    '''
    def __init__(self):
        self.base_url = "https://www.kuaidaili.com/free/inha/{page}/"

    @log_exception
    def getIps(self, page):
        url = self.base_url.format(page=page)
        html = my_requests.get_html(url, headers, "utf-8")
        if html is None:
            return None
        doc = PyQuery(html)
        ips_list = doc(".table.table-bordered.table-striped tbody tr")
        for ips_info in ips_list.items():
            ip = ips_info("td[@data-title='IP']").text()
            port = ips_info("td[@data-title='PORT']").text()
            type = ips_info("td[@data-title='类型']").text()
            # logging.info(f"快代理-{ip}-{port}-{type}")
            yield ip, port, type

class KaiXinProxies:
    def __init__(self):
        self.base_url = "http://www.kxdaili.com/dailiip/1/{page}.html"

    @log_exception
    def getIps(self, page):
        url = self.base_url.format(page=page)
        html = my_requests.get_html(url, headers, "UTF-8")
        if html is None:
            return None
        doc = PyQuery(html)
        ips_list = doc(".hot-product-content .active tbody tr")
        for ips_info in ips_list.items():
            ip = ips_info("td:first-child").text()
            port = ips_info("td:nth-child(2)").text()
            type = ips_info("td:nth-child(4)").text()
            yield ip, port, type

class TaiYangProxies():
    def __init__(self):
        self.base_url = "http://www.taiyanghttp.com/free/page{page}/"

    @log_exception
    def getIps(self, page):
        url = self.base_url.format(page=page)
        html = my_requests.get_html(url, headers, "utf-8")
        if html is None:
            return None
        doc = PyQuery(html)
        ips_list = doc(".tr.ip_tr div") #document.querySelector("#ip_list > div:nth-child(1) > div:nth-child(1)")
        ips_info = [ips_info("div").text() for ips_info in ips_list.items()]

        for i in range(0, len(ips_info)//9):
            ip = ips_info[0+9*i]
            port = ips_info[1+9*i]
            type = ips_info[6+9*i]
            # logging.info(f"太阳代理-{ip}-{port}-{type}")
            yield ip, port, type

async def run1():
    for page in range(1, 11):
        for ip, port, type in kaixin.getIps(page):
            logging.info(f"开心代理{ip}-{port}-{type} - 检测")
            sql_m.insert_info(ip, port, type)
            await asyncio.sleep(4)
        await asyncio.sleep(17)

async def run2():
    for page in range(1, 200):
        for ip, port, type in kuai.getIps(page):
            logging.info(f"快代理-{ip}-{port}-{type} - 检测")
            sql_m.insert_info(ip, port, type)
            await asyncio.sleep(2)
        await asyncio.sleep(15)

async def run3():
    for page in range(1, 20):
        for ip, port, type in taiyang.getIps(page):
            logging.info(f"太阳代理{ip}-{port}-{type} - 检测")
            sql_m.insert_info(ip, port, type)

            await asyncio.sleep(3)
        await asyncio.sleep(26)
def all_run():
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(asyncio.wait([run1(), run2(), run3()]))
    loop.close()


if __name__ == '__main__':
    kuai = KuaiProxies()
    kaixin = KaiXinProxies()
    taiyang = TaiYangProxies()
    engine = create_engine("mysql+pymysql://root:{}@{}:{}/{}?charset=UTF8MB4". \
                           format(mysql_pwd, mysql_host, mysql_port,
                                  mysql_db), pool_recycle=int(mysql_port),
                           pool_size=0, max_overflow=-1)
    DBSession = sessionmaker(bind=engine)  # 创建session类型
    sql_m = MysqlServer(DBSession)
    while True:
        all_run()
        print("-"*200)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(60*60*24)


