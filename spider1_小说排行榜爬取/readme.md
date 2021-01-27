# readme

- 这是一个十分简单的入门案例，案例内容就是获取一个小说网中对于月票排行榜的小说推荐。

# 使用库

- requests
  - 这是一个第三方库，需要进行pip安装
  - 用来发起请求和获取响应
- pyquery
  - 这是一个第三方库，需要pip安装
  - 进行数据解析
- json
  - 数据存储
- loging
  - 日志信息输出

# IP代理

为了防止自己的IP被关小黑屋，就用了一些免费的代理，需要的话可以去：https://ip.ihuan.me/address/5Lit5Zu9.html

但是不要用虫子爬，站猪也不容易

# 代码详解

1. 引入对应的库

```python
import requests
from pyquery import PyQuery
import logging
import json
```

2. 设置日志的参数，**level**:设置日志的等级，**format**：设置日志的输出格式

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

3. **start_url**：这个是目标地址，进行网页查看后发现月票榜一共有10页，**url**的变化只是**p={page}**，网页有简单的反爬手段，需要在发起请求的时候携带请求头。

```python
start_url = 'http://www.zongheng.com/rank/details.html?rt=1&d=1&i=2&p={page}'#网页地址

#请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
```

4. 发起请求，然后将获取的网页源码返回，代码中的重点在于```response = requests.get(url=url, headers=headers, proxies=proxies,  verify=False)```利用get发起请求。

   1. url:目标网页
   2. headers:请求头
   3. proxies:代理ip，注意这里需要传入的数据格式为字典，且不需要手动切换，ip请求失败之后，会帮我们自动切换，知道获取响应
   4. verify:SSL验证设置为False。如果不明白SSL是什么，可以去度娘看https://baike.baidu.com/item/ssl/320778?fr=aladdin

   **对于requests的详细内容可以查看文档：https://requests.readthedocs.io/en/master/**

```python
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
```

5. 主要功能是将获取的网页源码传入，利用pyquery进行数据的提取。
   1. PyQuery是一个类似于jQuery的解析网页工具，使用lxml操作xml和html文档，语法和jQuery很像。
   2. 详细的情况可以查看：**https://github.com/gawel/pyquery**

```python
def get_detail(text):
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
```

6. 执行部分。

```python
if __name__ == '__main__':

    proxies = dict() #存放读取的代理ip
    books_info = {"info":list()}#将来的信息存储在字典中
    for i in json.load(open('./m_proxies.json'))['proxies']:
        proxies.update({"https":i})
        
    for i in range(1,11):#爬取10页的内容
        text = get_page(start_url.format(page=i), proxies)
        books_info["info"].append(get_detail(text))
    
    #将获取的内容写入json文件
    json.dump(books_info, open('books_info.json', 'a+', encoding='utf-8'), ensure_ascii=False, indent=4)
```


