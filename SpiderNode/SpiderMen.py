from multiprocessing.managers import BaseManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
import time


class SpiderWork(object):
    def __init__(self):
        # 初始化分布式进程中工作节点的连接工作
        # 实现第一步：使用 BaseManager 注册用于获取 Queue 的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 实现第二步：连接到服务器
        server_addr = '127.0.0.1'
        print('Connect to server %s...' % server_addr)
        # 注意保持端口和验证口令与服务进程设置的完全一致
        self.m = BaseManager(address=(server_addr, 8001), authkey='baike'.encode('utf-8'))
        # 从网络连接
        self.m.connect()
        # 实现第三步：获取 Queue 的对象
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        # 初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    print('获取将要爬取的url链接：')
                    url = self.task.get()
                    if url == 'end':
                        # 接着通知其他节点停止工作
                        while not self.task.empty():
                            print('获取url链接')
                            url = self.task.get()
                            print(url)
                            print('爬虫节点正在解析:%s' % url.encode('utf-8'))
                            content2 = self.downloader.download(url)
                            new_urls, data = self.parser.parser(url, content2)
                            print('放入新连接和内容')
                            print(data)
                            self.result.put({"new_urls": new_urls, "data": data})
                        print('爬虫节点收到控制节点通知停止工作...')
                        self.result.put({'new_urls': None, 'data': 'end'})
                        return
                    print(url)
                    print('爬虫节点正在解析:%s' % url.encode('utf-8'))
                    content2 = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content2)
                    print('放入新连接和内容')
                    self.result.put({"new_urls": new_urls, "data": data})
                else:
                    time.sleep(0.5)
            except EOFError:
                print("连接工作节点失败")
                return
            except Exception as e:
                print(e)
                print('Crawl  fail ')
                return


if __name__ == "__main__":
    spider = SpiderWork()
    spider.crawl()
