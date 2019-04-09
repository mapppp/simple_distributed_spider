from DataOutPut import DataOutput

datas = [{'url': 'http://qq.ip138.com/tianqi/', 'title': '123', 'summary': 'fhdnjasik'}, {'url': 'http://qq.ip138.com/shenfenzheng/', 'title': '432', 'summary':'fjisadalshfnvjk'}, {'url':'http://qq.ip138.com/huoche/', 'title':'765', 'summary':'djailnfva'}, {'url':'http://qq.ip138.com/daishoudian/mobile.htm', 'title':'876', 'summary':'fjdioashfudin'}, {'url':'http://www.miitbeian.gov.cn/', 'title':'4df', 'summary':'fghsdjakfbjdsa'}]
num = 4
data_out_put = DataOutput()
# 将数据一个一个的保存，获得一个数据调用一次store_data()
for data in datas:
    data_out_put.store_data(data, num=num)
data_out_put.ouput_end()
