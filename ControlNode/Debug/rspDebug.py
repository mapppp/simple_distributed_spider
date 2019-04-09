import time
from multiprocessing import Queue, Process


def result_solve_proc(result_q, conn_q, store_q):
    """
    :param result_q: 里面放的是字典，有两个字段，一个是new_urls，一个是data
    :param conn_q:里面放的是url集合
    :param store_q:
    :return:
    """
    while True:
        try:
            if not result_q.empty():
                content = result_q.get(True)
                if content['new_urls'] == 'end':
                    # 结果分析进程接收通知然后结束
                    print('结果分析进程接收通知然后结束!')
                    store_q.put('end')
                    break
                # url 为 set 类型 解析出来的数据为 dict 类型
                conn_q.put(content['new_urls']), store_q.put(content['data'])
            else:
                # print('等待爬虫节点响应')
                time.sleep(0.1)  # 延时休息
        except:
            time.sleep(0.1)  # 延时休息


def put_res_proc(result_q):
    rs = [{'new_urls': '3', 'data': {"3": "6"}}, {'new_urls': 'end', 'data': {"5": "6"}}]
    for r in rs:
        print(r)
        result_q.put(r)


def get_urls_q(conn_q):
    while True:
        if not conn_q.empty():
            print(conn_q.get())
        else:
            time.sleep(1.0)


def get_data_proc(store_q):
    while True:
        if not store_q.empty():
            print(store_q.get())
        else:
            time.sleep(1.0)


if __name__ == "__main__":
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    r_s_p = Process(target=result_solve_proc, args=(result_q, conn_q, store_q,))
    res_d = Process(target=put_res_proc, args=(result_q,))
    conn_d = Process(target=get_urls_q, args=(conn_q,))
    sto_d = Process(target=get_data_proc, args=(store_q,))
    r_s_p.start()
    res_d.start()
    conn_d.start()
    sto_d.start()


