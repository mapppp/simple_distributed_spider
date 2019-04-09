from multiprocessing import Process, Queue
from multiprocessing.managers import BaseManager
import time


def create_q(url_q, result_q):
    try:
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        m = BaseManager(address=('', 8001), authkey='baike'.encode('utf-8'))
        print('成功创建q')
        return m
    except Exception as e:
        print(e)


def put_url(url_q, urls=None):
    # i = 0
    # while True:
    #     if url is not None:
    #         url_q.put(url)
    #         i += 1
    #         url = None
    #         print('放入url')
    #     else:
    #         if i == 1:
    #             url_q.put('end')
    #             break
    #         print('请放入url')
    #         time.sleep(0.1)
    i = 0
    while True:
        if urls is not None:
            for url in urls:
                print("放入url：", url)
                url_q.put(url)
                i += 1
            urls = None
        else:
            if i == 3:
                url_q.put('end')
                break
            print('请放入url')
            time.sleep(0.1)


def get_result(result_q):
    while True:
        # print(result_q.empty())
        if not result_q.empty():
            data = result_q.get()
            content = data['data']
            urls = data['new_urls']
            print('获取到的url: ', urls, '数据: ', content)
        else:
            time.sleep(0.5)


if __name__ == '__main__':
    url_q = Queue()
    result_q = Queue()
    urls = {'http://www.17k.com/book/2722530.html', 'http://www.17k.com/book/2961718.html','http://www.17k.com/book/2911081.html'}
    print('创建q')
    m = create_q(url_q, result_q)
    print('创建进程')
    url_put_proc = Process(target=put_url, args=(url_q, urls,))
    result_get_proc = Process(target=get_result, args=(result_q,))
    print('启动进程')
    url_put_proc.start()
    result_get_proc.start()
    print('连接')
    m.get_server().serve_forever()
