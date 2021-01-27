'''
2020-12-27 兰州 晴
运气,就是机会碰巧撞到了你的努力。
爬取堆图网的萌宠头像的图片。将图片保存到本地
'''

import requests
from pyquery import PyQuery
import logging
import time
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levlename)s - %(message)s"
)

#请求头
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

def get_html(url):
    try:
        response = requests.get(url=url,  headers=headers)
        response.encoding = "utf-8"
        if response.status_code != 200:
            logging.info(f"get {url} not 200")
            return None
        return response
    except Exception as e:
        logging.error(f"{e}-{url} get html error")

def get_images_url(html):
    if html is None:
        logging.info(f"get html is None")
        return None
    doc = PyQuery(html)
    images = doc("img")
    for image in images.items():
        image_url = image("img").attr("src")
        image_name = image("img").attr("alt")
        if image_name is None:
            continue
        yield image_url

def image_save(response, name):
    with open("./image/{}.jpeg".format(name), "wb") as f:
        f.write(response.content)

if __name__ == '__main__':
    url = "https://www.duitang.com/search/?kw=%E8%90%8C%E5%AE%A0%E5%A4%B4%E5%83%8F&type=feed"
    html = get_html(url).text
    for i_url in get_images_url(html):
        res = get_html(i_url)
        image_save(res, time.time())
