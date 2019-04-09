# coding:utf-8
import time
from multiprocessing.managers import BaseManager
from DataOutPut import DataOutput
from URLManager import UrlManager
from multiprocessing import Process, Queue


class NodeManager(object):
    def start_Manager(self, url_q, result_q):
        """
        创建一个分布式管理器
        :param url_q: url 队列
        :param result_q: 结果队列
        :return:
        """
        # 把创建的两个队列注册在网络上，利用 register 方法，callable 参数关联了 Queue 对象，
        # 将 Queue 对象在网络中暴露
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        # 绑定端口8001，设置验证口令“baike”。这个相当于对象的初始化
        manager = BaseManager(address=('', 8001), authkey='baike'.encode('utf-8'))
        # 返回 manager 对象
        return manager

    def url_manager_proc(self, url_q, conn_q, root_url, num=200):
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while url_manager.has_new_url():
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                if url_manager.old_url_size() > num:
                    # 通知爬行节点工作结束
                    url_q.put('end')
                    print('控制节点发起结束通知!')
                    # 关闭管理节点，同时存储 set 状态
                    url_manager.save_progress()
                    return
            # 没有url了就从conn_q里拿
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
                else:
                    # 延时休息
                    time.sleep(0.1)
            except Exception as e:
                print(e)

    # spider_man.crawl("http://www.17k.com/man/")

    def result_solve_proc(self, result_q, conn_q, store_q):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['data'] == 'end':
                        # 结果分析进程接收通知然后结束
                        print('结果分析进程接收结束通知!')
                        store_q.put('end')
                        return
                    # url 为 set 类型 解析出来的数据为 dict 类型
                    conn_q.put(content['new_urls']), store_q.put(content['data'])
                else:
                    # print('等待爬虫节点响应')
                    time.sleep(0.1)  # 延时休息
            except:
                time.sleep(0.1)  # 延时休息

    def store_proc(self, store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接受通知然后结束!')
                    # output.output_html()
                    output.ouput_end()
                    return
                print("储存获取的数据")
                print(data)
                output.store_data(data)
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    print("初始化4个队列")
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    print('创建分布式管理器')
    node = NodeManager()
    manager = node.start_Manager(url_q, result_q)
    print('创建 URL 管理进程、 数据提取进程和数据存储进程')
    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q,
                                                                   'http://www.17k.com/man/',))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q,
                                                                     conn_q, store_q,))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    print('启动3个进程和分布式管理器')
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    print("连接")
    manager.get_server().serve_forever()
