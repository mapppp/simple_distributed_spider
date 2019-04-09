from HtmlParser import HtmlParser
from HtmlDownloader import HtmlDownloader

html_downloader = HtmlDownloader()
root_url = 'http://www.17k.com/book/2722530.html'
html_text = html_downloader.download(root_url)
html_parser = HtmlParser()
new_urls, new_date = html_parser.parser(root_url, html_text)
print(new_urls, new_date)
