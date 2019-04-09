import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

'''
HtmlParser
parser()
'''

__all__ = ['HtmlParser']


class HtmlParser(object):
    def parser(self, page_url, html_cont):
        """
        解析网页内容，抽取url和数据
        :param page_url：当前下载页面的url
        :param html_cont：当前下载页面的网页内容
        """
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        """
        抽取新的 URL 集合
        :param page_url: 当前下载页面的 URL
        :param soup:soup
        :return: 返回新的 URL 集合
        """
        new_urls = set()
        # 抽取符合要求的 a 标记
        links = soup.find_all('a', href=re.compile(r'http://www.17k.com/book/\d+'+r'\.html'))
        for link in links:
            # 提取href属性
            new_url = link['href']
            # print(new_url)
            # 拼接成完整网址
            new_full_url = urljoin(page_url, new_url)
            # print(new_full_url)
            new_urls.add(new_full_url)
        print('新url集合长度'+str(len(new_urls)))
        return new_urls

    def _get_new_data(self, page_url, soup):
        """
        抽取有效数据
        :param page_url:下载页面的 URL
        :param soup:
        :return:返回有效数据
        """
        data = {'url': page_url}
        print('parsing ', page_url)
        if soup.find('div', class_='Info Sign'):
            title = soup.find('div', class_='Info Sign').find('h1').find('a')
            content1 = soup.find('div', class_='Info Sign').find('div', class_='cont').find('a')
            if content1:
                data['summary'] = content1.get_text()
            else:
                data['summary'] = ''
            if title:
                data['title'] = title.get_text()
            else:
                data['title'] = ''
        else:
            data['summary'] = ''
            data['title'] = ''
        return data
