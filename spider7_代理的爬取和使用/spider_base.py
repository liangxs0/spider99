import requests
from m_log import *
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class MyRquests(object):

    @log_exception
    def get_html(self, url, headers, encode):
        response = requests.get(url=url, headers=headers)
        response.encoding = encode
        if response.status_code !=200:
            logging.info(f"网页请求失败 - {url}")
            return None
        logging.info(f"{url}")
        return response.text


my_requests = MyRquests()

