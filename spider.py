"""
    该项目为静态页面爬取
"""
import requests
from lxml import etree
from fake_useragent import UserAgent

import random
import os

from threading import Thread
from queue import Queue


from proxy_list import GetProxyList

class CodeSpider():
    '''
        根据网页结构创建文件夹，爬取网页中的文件存入对应文件夹
        使用IP代理，fake UserAgent，xpath表达式，递归思想,多线程
    '''
    def __init__(self,url,auth,directory):
        self.url = url
        self.auth = auth
        self.ua = UserAgent().random
        self.directory = directory
        # 创建url队列
        self.url_queue = Queue()
        self.url_list = [] # url列表，用于打印输出

    def get_page(self, url):
        '''
            获取byte数据类型页面信息
        :return: html_byte
        '''
        proxy_list = GetProxyList('ip_prot.csv')
        proxy = random.choice(proxy_list.getproxiselist())
        print(proxy)
        # proxy = {'https': 'https://121.225.186.55:3000', 'http': 'http://121.225.186.55:3000'}

        html_byte = requests.get(
            url=url,
            auth = self.auth,
            headers = {'User-Agent':self.ua},
            proxies = proxy,
            # timout = 5
        ).content
        return html_byte

    def parse_page(self,html_byte):
        '''
            解析页面，返回url列表，本案例中的各级页面xpath表达式相同
        :param html_byte:
        :return:
        '''
        page_info = etree.HTML(html_byte.decode('utf-8','ignore')) # 节点对象
        url_list = page_info.xpath('//a/@href')[1:] # 去除第一个元素，获得url列表
        return url_list

    def get_url_queue(self, url):
        '''
            获取各级页面的url
        :param url:
        :return:
        '''
        html_byte = self.get_page(url)
        href_list = self.parse_page(html_byte)

        for href in href_list:
            url_new = url + href
            if href.endswith('/'):
                self.get_url_queue(url_new)
            else:
                self.url_queue.put(url_new)
                self.url_list.append(url_new)
            url_new = url

    def download_data(self):
        '''
            线程对象从队列中获取url,执行线程，
            队列取完后跳出循环，避免死循环堵塞
        :return:
        '''
        while True:
            if self.url_queue.empty():
                break
            else:
                url = self.url_queue.get() # 从序列中获取
                directory = self.directory + '/'.join(url.split('/')[5:-1])
                filename = self.directory + '/'.join(url.split('/')[5:])

                if not os.path.exists(directory):
                    os.makedirs(directory)

                html_byte = self.get_page(url)
                try:
                    with open(filename,'wb') as f:
                        f.write(html_byte)
                    print(filename,'下载成功')
                except:
                    print('*' * 50, filename, '下载失败！')
                    pass

    def main(self):
        '''
            创建线程队列，开启线程，爬取数据，回收线程结果
        :return:
        '''
        # url入队列
        self.get_url_queue(self.url)
        print(self.url_list)
        # 创建多线程
        t_list = [] # 用统一join
        for i in range(10): # 开启20个线程
            t = Thread(target=self.download_data) # 线程执行target对象
            t_list.append(t) # 线程对象存入队列
            t.start() # 开启线程
        # 阻塞等待，回收线程
        for i in t_list:
            i.join()

if __name__ == '__main__':
    url = 'http://code.tarena.com.cn/AIDCode/aid1907/'
    auth = ('tarenacode', 'code_2013')
    directory = 'E:/Python视频/测试/'
    p = CodeSpider(url, auth, directory)
    p.main()
