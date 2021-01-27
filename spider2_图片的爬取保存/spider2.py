'''
2020-12-15, 🌤， 包头
'''

from requests_html import HTMLSession
import logging
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

session = HTMLSession()
def get_page(url, session):
    '''
    获取页面
    :param url:页面的url
    :param session: HTMLSession对象
    :return:请求成功返回HTMLResponse对象，否则返回None
    '''

    response = session.get(url=url, headers=headers)
    if response.status_code == 200:
        logging.info('发起请求 %s'%url)
        return response
    else:
        logging.error('请求失败 %s'%url)
        return None

def get_detail(response):
    images = {"info":list()}
    images_info = response.html.find('.tbox dd .d1.ico3 li')
    for image in images_info:
        image_info = image.find('a img', first=True).attrs
        yield image_info

def save_image(response, path):
    with open(path, 'wb+') as f:
        f.write(response.content)
        logging.info(f"{path}存储完成")


def main():
    path = './image/{image_name}.jpg'
    url = 'https://www.tupianzj.com/meinv/mm/meizitu/'
    session = HTMLSession()

    response = get_page(url, session)
    for image_info in get_detail(response):
        image_res = get_page(image_info['src'], session)
        if image_res is None:
            continue
        save_image(image_res, path.format(image_name=image_info['alt']))

if __name__ == '__main__':
    main()




