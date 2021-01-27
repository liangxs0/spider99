'''
2020-12-14 ,🌤，包头
'''
import requests
from pyquery import PyQuery
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

start_url = 'http://www.zongheng.com/rank/details.html?rt=1&d=1&i=2&p={page}'#网页地址

#请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

def get_page(url, proxies):
    '''
    获取页面代码
    :param url: 页面连接
    :param proxies: 代理ip,字典格式
    :return: 页面的代码内容
    '''
    #发起请求
    response = requests.get(url=url, headers=headers, proxies=proxies,  verify=False)
    #响应状态判断
    if response.status_code == 200:
        logging.info("获取页面：%s"%url)
        return response.text #返回页面源码
    else:
        logging.info("页面获取失败：%s"%url)
        return None


def get_detail(text):
    if text is None:
        return None
    #获取pyquery对象，将下载的网页代码传入
    doc = PyQuery(text)
    #获取信息块
    book_lists = doc('.rankpage_box div')
    for book_info in book_lists.items():
        book_name = book_info('.rank_d_list.borderB_c_dsh.clearfix .rank_d_book_intro.fl .rank_d_b_name').attr('title')
        book_url = book_info('.rank_d_list.borderB_c_dsh.clearfix .rank_d_book_intro.fl .rank_d_b_name a').attr('href')
        author_name =  book_info('.rank_d_list.borderB_c_dsh.clearfix .rank_d_book_intro.fl .rank_d_b_cate').attr('title')
        if book_name is None:
            continue
        return {
            '书名':book_name,
            '作者':author_name,
            '链接':book_url
        }


if __name__ == '__main__':

    proxies = dict() #存放读取的代理ip
    books_info = {"info":list()}#将来的信息存储在字典中
    for i in json.load(open('./m_proxies.json'))['proxies']:
        proxies.update({"https":i})

    for i in range(1,11):#爬取10页的内容
        text = get_page(start_url.format(page=i), proxies)
        if text is None:
            continue
        books_info["info"].append(get_detail(text))

    #将获取的内容写入json文件
    json.dump(books_info, open('books_info.json', 'a+', encoding='utf-8'), ensure_ascii=False, indent=4)


