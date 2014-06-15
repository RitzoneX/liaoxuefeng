# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
from pprint import pprint
import re
import os

def filename(url):
    """文件名"""
    name = '/'.join(url.split('/')[3:])
    return name if name[-1] != '/' else name[:-1]

def htmlname(url):
    """Html文件名"""
    return filename(url) + '.html'

def makedirs(url):
    """创建目录"""
    url = url if url[-1] != '/' else url[:-1]
    p = path(url)
    if p != '' and (not os.path.exists(p)):
        os.makedirs(p)

def path(url):
    return '/'.join(url.split('/')[3:-1])


class Html:
    """Html页面"""
    
    def __init__(self, url):
        self.url = url
        data = urllib.urlopen(url).read().replace('="//', '="http://')
        self.soup = BeautifulSoup(data.replace('="/', '="http://www.liaoxuefeng.com/'))      

    def download(self):
        """下载页面"""
        self.downloadFiles()
        self.downloadHtml()
        
    def downloadFiles(self):
        """下载页面所需文件"""
        for url in self.findUrls():
            self.downloadFile(url)
            
    def findUrls(self):
        """查找页面资源url"""
        urls = [x['href'] for x in self.link()]
        urls += [x['src'] for x in self.src()]
        urls += [x['data-src'] for x in self.data_src()]
        return urls
    
    def link(self):
        return self.soup('link')
    
    def src(self):
        return self.soup(src=re.compile(r'http[^?]*$'))
    
    def data_src(self):
        return self.soup(attrs={'data-src':True})
        
    def downloadFile(self, url):
        """下载url中的文件"""
        if not os.path.exists(filename(url)):
            makedirs(url)
            urllib.urlretrieve(url, filename(url))

    def downloadHtml(self):
        """下载Html文件"""
        makedirs(self.url)
        self.replace()
        with open(htmlname(self.url), 'wb') as f:
            f.write(str(self.soup))
        
    def replace(self):
        """替换url"""
        for tag in self.link():
            self.sub(tag, 'href')
        for tag in self.src():
            self.sub(tag, 'src')
        for tag in self.data_src():
            self.sub(tag, 'data-src')
        # 修改 href
        for tag in self.soup(href=re.compile(r'http://www.liaoxuefeng.com/wiki/')):
            tag['href'] = self.mainPath() + tag['href'][27:] + '.html'
    
    def sub(self, tag, attr):
        if tag[attr][-1] == '/':
            tag[attr] = tag[attr][:-1]
        tag[attr] = re.compile(r'http://.*?/').sub(self.mainPath(), tag[attr])
    
    def mainPath(self):
        """根据url返回顶层路径"""
        s = ''
        for i in range(len(self.url.split('/')) - 4):
            s += '../'
        return s

class Htmls(Html):
    """Html主页面"""
    def __init__(self, url):
        Html.__init__(self, url)
        
    def download(self):
        self.downloadOther()
        Html.download(self)
    
    def downloadOther(self):
        """下载其他页面"""
        for url in self.links():
            if not os.path.exists(htmlname(url)):
                Html(url).download()
    
    def links(self):
        """查找其他链接"""
        return [tag['href'] for tag in self.soup.find(class_='x-wiki-tree')('a')]
    
pythonUrl = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000'
gitUrl = 'http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000'
Htmls(pythonUrl).download()
Htmls(gitUrl).download()
print 'finish'