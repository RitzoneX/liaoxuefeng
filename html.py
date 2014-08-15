# -*- coding: utf-8 -*-

import os
import re
import urllib2
import logging
from pprint import pprint
import requests

path = 'liaoxuefeng'

headers = {'Accept-Language': 'zh-CN,zh;q=0.8'}


class Html(object):

    """docstring for Html"""

    def __init__(self, url):
        super(Html, self).__init__()
        self.url = url
        self.initHtml()
        self.initUrls()

    def initHtml(self):
        while True:
            try:
                request = urllib2.Request(self.url, headers=headers)
                response = urllib2.urlopen(request, timeout=5)
                data = response.read().replace('="//', '="http://')
                mainUrl = '/'.join(self.url.split('/')[:3]) + '/'
                self.html = data.replace('="/', '="' + mainUrl)
            except Exception, e:
                logging.error('%s: %s' % (e, self.url))
            else:
                break
        

    def initUrls(self):
        l = re.findall(r'<link.*?>|src="http.*?"', self.html)
        pattern = re.compile(r'http[^"]*')
        self.urls = [pattern.search(x).group() for x in l]

    def download(self):
        self.downloadFiles()
        self.downloadHtml()

    def downloadFiles(self):
        for url in self.urls:
            downloadFile(url)

    def downloadHtml(self):
        self.html = self.html.replace(
            'href="http:/', 'href="' + self.relativePath())
        self.html = self.html.replace(
            'src="http:/', 'src="' + self.relativePath())
        self.html = re.sub(r'(wiki[^"]*/\w{50})"', r'\1.html"', self.html)
        self.html = re.sub(r'(src=".*?)/"', r'\1"', self.html)

        htmlname = self.getHtmlname()
        if not os.path.exists(htmlname):
            logging.debug('download url: %s' % self.url)
            makedirs(htmlname)
            with open(htmlname, 'wb') as f:
                f.write(self.html)

    def getHtmlname(self):
        return getFilename(self.url) + '.html'

    def relativePath(self):
        """获取相对路径"""
        path = '/'.join(self.url.split('/')[2:-1])
        return re.sub(r'[^/]*', '..', path)


def downloadFile(url):
    """下载文件"""
    filename = getFilename(url)
    if not os.path.exists(filename):
        logging.debug('download file: %s' % filename)
        makedirs(filename)
        urlretrieve(url, filename)
        # urllib.urlretrieve(url, filename)

requests.adapters.DEFAULT_RETRIES = 5


def urlretrieve(url, filename):
    while True:
        try:
            r = requests.get(url, timeout=5)
            with open(filename, "wb") as code:
                code.write(r.content)
        except Exception, e:
            logging.error(e)
        else:
            break


def getFilename(url):
    """获取文件名"""
    url = url.split('?')[0]
    url = url if url[-1] != '/' else url[:-1]
    return path + '/' + '/'.join(url.split('/')[2:])


def makedirs(filename):
    """创建文件目录"""
    dir = '/'.join(filename.split('/')[:-1])
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':
    url = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001402402473485d8c205b735ee4e698f90769960fcec4b000'
    logging.basicConfig(level=logging.DEBUG)
    Html(url).download()
    # url = 'http://www.liaoxuefeng.com/files/attachments/001399877306431ffee0ff7d3fe48bb88da759bb977c1e0000'
    # urlretrieve(url, 'tttt')
