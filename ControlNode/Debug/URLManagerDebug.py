from URLManager import UrlManager
import pickle
import hashlib


print("has_new_url", UrlManager.has_new_url.__doc__)
print("add_new_url", UrlManager.add_new_url.__doc__)
print("add_new_urls", UrlManager.add_new_urls.__doc__)
print("get_new_url", UrlManager.get_new_url.__doc__)
print("new_url_size", UrlManager.new_url_size.__doc__)
print("old_url_size", UrlManager.old_url_size.__doc__)
print("save_progress", UrlManager.save_progress.__doc__)
print("load_progress", UrlManager.load_progress.__doc__)

urls = set(["http://qq.ip138.com/tianqi/", "http://qq.ip138.com/shenfenzheng/", "http://qq.ip138.com/huoche/", "http://qq.ip138.com/daishoudian/mobile.htm", "http://www.miitbeian.gov.cn/"])
urlmanager = UrlManager()
print(type(urls))
# urlmanager获得新的url集合
urlmanager.add_new_urls(urls)
print(urlmanager.has_new_url())
# urlmanager输出一个未爬取的url
new_url = urlmanager.get_new_url()  #拿出的同时将其放的到已经爬取的url集合中
# 没有未爬取的url时返回None
print(new_url)
print(urlmanager.old_url_size())
# 保存进度
urlmanager.save_progress()