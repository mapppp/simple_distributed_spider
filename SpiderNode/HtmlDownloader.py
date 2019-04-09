import requests


class HtmlDownloader(object):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
        self.headers = {'User-Agent': self.user_agent}

    def download(self, url):
        if url is None:
            return
        try:
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print('成功下载html')
            return r.text
        except Exception as e:
            print(e)
