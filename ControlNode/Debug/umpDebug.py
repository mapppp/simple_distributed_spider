from multiprocessing import Process, Queue
from URLManager import UrlManager
import time


def url_manager_proc(url_q, conn_q, root_url, num=6):
    """
    :param url_q:里面放的是url集合单个url
    :param conn_q:里面放的是url集合
    :param root_url:
    :param num:
    :return:
    """
    url_manager = UrlManager()
    url_manager.add_new_url(root_url)
    while True:

        while url_manager.has_new_url():
            print("# url_manager_proc将要爬取的url放入url_q中")
            new_url = url_manager.get_new_url()
            print(new_url)
            url_q.put(new_url)
            if url_manager.old_url_size() > num:
                # 通知爬行节点工作结束
                url_q.put('end')
                print('控制节点发起结束通知!')
                # 关闭管理节点，同时存储 set 状态
                url_manager.save_progress()
                break
        try:
            if not conn_q.empty():
                print("# url_manager_proc从conn_q中拿取urls")
                urls = conn_q.get()
                print(urls)
                url_manager.add_new_urls(urls)
            else:
                # 延时休息
                time.sleep(0.1)
        except Exception as e:
            print(e)


def url_debug_proc(url_q):
    while True:
        if not url_q.empty():
            url_q.get()
        else:
            time.sleep(1.0)


def conn_debug_proc(conn_q):
    for urls in [["11", "22", "33", "44", "55"], ["66", "77"]]:
        conn_q.put(urls)


if __name__ == "__main__":
    url_q = Queue()
    conn_q = Queue()
    url_m = Process(target=url_manager_proc, args=(url_q, conn_q, 'http://www.17k.com/man/',))
    url_d = Process(target=url_debug_proc, args=(url_q,))
    conn_d = Process(target=conn_debug_proc, args=(conn_q,))
    url_m.start()
    url_d.start()
    conn_d.start()
