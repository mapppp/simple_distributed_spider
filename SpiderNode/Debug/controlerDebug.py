import time
from multiprocessing.managers import BaseManager


def connect():
    # 初始化分布式进程中工作节点的连接工作
    # 实现第一步：使用 BaseManager 注册用于获取 Queue 的方法名称
    BaseManager.register('get_task_queue')
    BaseManager.register('get_result_queue')
    # 实现第二步：连接到服务器
    server_addr = '127.0.0.1'
    print('Connect to server %s...' % server_addr)
    # 注意保持端口和验证口令与服务进程设置的完全一致
    m = BaseManager(address=(server_addr, 8001), authkey='baike'.encode('utf-8'))
    # 从网络连接
    m.connect()
    # 实现第三步：获取 Queue 的对象
    task_q = m.get_task_queue()
    result_q = m.get_result_queue()
    # 初始化网页下载器和解析器
    print('connected')
    return task_q, result_q


def put_result(result_q):
    n_datas = [{"url": "1", "title": "2", "summary": "3"}, {"url": "4", "title": "5", "summary": "6"}, {"url": "7", "title": "8", "summary": "9"}]
    url = 1
    for n_data in n_datas:
        data = {"new_urls": {str(url), }, "data": n_data}
        url += 1
        print("爬虫节点返回的数据：p", data)
        result_q.put(data)


def get_url(task_q,result_q):
    while True:
        if not task_q.empty():
            url = task_q.get()
            print("爬虫节点获取到的url：g", url)
            if url == "end":
                result_q.put({"new_urls": {"end", }, "data": "end"})
        else:
            time.sleep(0.5)


if __name__ == "__main__":
    task_q, result_q = connect()
    put_result(result_q)
    get_url(task_q, result_q)
