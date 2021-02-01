import requests
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class MyRquests(object):
    def get_html(self, url, headers, encode):
        try:
            response = requests.get(url=url, headers=headers)
            response.encoding = encode
            if response.status_code !=200:
                logging.info(f"网页请求失败 - {url}")
                return None
            logging.info(f"{url}")
            return response.text
        except Exception as e:
            logging.info(f"网页请求发生异常 - {url}")
            return None

my_requests = MyRquests()

