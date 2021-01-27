'''
2020-12-27 兰州 晴
人在旅途，难免会遇到荆棘和坎坷，但风雨过后，一定会有美丽的彩虹。
爬虫功能，获取自己的ip所在地区，然后获取当前地图的气候信息
为了帮领导写了demo，今天做了完善
'''

import requests
from pyquery import PyQuery
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#请求头
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

def get_html(url):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = "utf-8"
        if response.status_code != 200:
            logging.info(f"get html not 200 {url}")
            return None
        logging.info(f"get html {url}")
        return response
    except Exception as e:
        logging.error(f"get html error {e} - {url}")

def get_address(html):
    if html is None:
        logging.info("address html is None")
        return None
    doc = PyQuery(html)
    infos = doc(".IpMRig-tit dd")
    return [info("dd").text() for info in infos.items()][0:2]

def get_city_id(city):
    with open("id.json", "r", encoding="utf-8") as fb:
        city_json = json.load(fb)["ids"][0]
    for c in city_json.keys():
        if c in city:
            logging.info(f"city:{c}")
            return city_json[c]
    return None

def get_weather(response):
    info = response.json()
    logging.info(f"天气信息{info}")


if __name__ == '__main__':
    address_url = "https://ip.tool.chinaz.com/"
    weather_url = 'http://www.weather.com.cn/data/sk/{}.html'
    html = get_html(address_url).text
    address_info = get_address(html)
    address_ip = address_info[0]
    address = address_info[1].split(' ')[0]
    logging.info(f"ip:{address_ip} address:{address}")
    while True:
        city_id = get_city_id(address)
        if city_id is None:
            address = input("please input city_name：")
        if city_id is not None:
            break
    print(city_id)
    weather_html = get_html(weather_url.format(city_id))
    get_weather(weather_html)


