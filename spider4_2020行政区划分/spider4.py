'''
2020-12-26 兰州 晴
盛年不重来,一日难再晨。及时当勉励,岁月不待人
爬取2020年我国各个行政区的划分
最后保存到一个json文件中
'''

import  requests
import logging
from pyquery import PyQuery
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#请求头
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

start_url = "http://www.xzqh.org/html/list/10100.html"

def get_html(url):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = 'gbk'
        if response.status_code != 200:
            logging.error(f"html get error {url}")
            return None
        return response.text
    except Exception as e:
        logging.error(f"html get error {url} - {e}")
        return None

def get_menu(html):
    base_url = "http://www.xzqh.org/html/"
    if html is None:
        return None
    doc = PyQuery(html)
    pro_city_lists = doc("#list_l2 div:nth-child(3) .boxmargin .List-2 li:gt(1)")
    for pro_cit in pro_city_lists.items():
        pro_name = pro_cit("a").text()
        pro_url = urljoin(base_url, pro_cit("a").attr("href"))
        yield pro_url

def get_detail(detail_html):
    if detail_html is None:
        return None
    doc = PyQuery(detail_html)
    infos = doc("#show .content br")
    for info in infos.items():
        res = info("br")
        res = str(res).replace("<br />&#13;", "").replace("  ","").replace("<br />&#13;", "").replace("\n", "").replace(u"\u3000", u"").replace(u"\xa0 ", u"").replace(u"\xa0", u"")
        if res == "":
            continue
        print(res.split("）"))

if __name__ == '__main__':
    html = get_html(start_url)
    for url in get_menu(html):
        detail_html = get_html(url)
        get_detail(detail_html)


