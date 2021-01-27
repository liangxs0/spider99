'''
2020-12-16, 🌤， 包头， 今天媳妇儿也到包头出差了,开心
'''

import requests
from pyquery import PyQuery
import logging
from urllib.parse import urljoin
import time
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

def get_page(url, proxies):
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        logging.info('页面获取-%s'%url)
        return response.text
    else:
        logging.error("页面获取失败 %s"%url)
        return None

def get_url(html):
    doc = PyQuery(html)
    base_url = 'https://movie.douban.com/subject/1292052/comments'
    next_url = urljoin(base_url, doc('#paginator .next').attr('href'))
    return next_url

def get_detail(html):
    doc = PyQuery(html)
    comment_list = doc('#comments .comment-item')
    for comment in comment_list.items():
        yield comment('.comment .comment-content .short').text()+'\n'


def main():
    url = 'https://movie.douban.com/subject/1292052/comments?status=P'

    proxies = dict()  # 存放读取的代理ip
    for i in json.load(open('./m_proxies.json'))['proxies']:
        proxies.update({"https": i})

    html = get_page(url, proxies)
    while True:
        if html is None:
            new_url = get_url(html)
            html = get_page(new_url, proxies)
            continue
        for comment in get_detail(html):
            with open("短评.txt", 'a+', encoding='utf-8') as f:
                f.write(comment)
        new_url = get_url(html)
        html = get_page(new_url, proxies)
        time.sleep(0.8)


if __name__ == '__main__':
    main()


