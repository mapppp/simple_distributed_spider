import time
from multiprocessing import Process,Queue
from DataOutPut import DataOutput


def store_proc(store_q):
    output = DataOutput()
    while True:
        if not store_q.empty():
            data = store_q.get()
            print(data)
            if data == 'end':
                print('存储进程接受通知然后结束!')
                output.output_html()
                output.ouput_end()
                return
            output.store_data(data)
        else:
            time.sleep(0.1)


def put_data_proc(store_q, datas):
    for data in datas:
        store_q.put(data)


if __name__ == "__main__":
    datas = [{"url": "1", "title": "2", "summary": "3"},{"url": "4", "title": "5", "summary": "6"},{"url": "7", "title": "8", "summary": "9"}, "end"]
    store_q = Queue()
    sp = Process(target=store_proc, args=(store_q,))
    pd = Process(target=put_data_proc, args=(store_q, datas))
    sp.start()
    pd.start()
