from SpiderNode.HtmlDownloader import HtmlDownloader

html_downloader = HtmlDownloader()
url = "http://www.baidu.com"
print(html_downloader.download(url))
