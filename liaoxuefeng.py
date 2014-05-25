# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
from pprint import pprint
import re
import os

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
        self.makedirs(url)
        if not os.path.exists(self.filename(url)):
            urllib.urlretrieve(url, self.filename(url))
    
    def filename(self, url):
        """文件名"""
        return '/'.join(url.split('/')[3:])
        
    def htmlname(self, url):
        """Html文件名"""
        return self.filename(url)
        
    def downloadHtml(self):
        """下载Html文件"""
        self.makeHtmldirs(self.url)
        self.replace()
        with open(self.htmlname(self.url), 'wb') as f:
            f.write(str(self.soup).replace('="http://www.liaoxuefeng.com/', '="../../'))
        
    def replace(self):
        """替换url"""
        for tag in self.link():
            self.sub(tag, 'href')
        for tag in self.src():
            self.sub(tag, 'src')
        for tag in self.data_src():
            self.sub(tag, 'data-src')
        # 修改 a href
        for tag in self.soup(href=re.compile(r'http://www.liaoxuefeng.com/wiki/[^/]*$')):
            tag['href'] += '/' + tag['href'].split('/')[-1]
    
    def sub(self, tag, attr):
        tag[attr] = re.compile(r'http://.*?/').sub('../../', tag[attr])
        
    def makedirs(self, url):
        """创建目录"""
        p = self.path(url)
        if p != '' and (not os.path.exists(p)):
            os.makedirs(p)
    
    def makeHtmldirs(self, url):
        """创建Html文件目录"""
        self.makedirs(url)

    def path(self, url):
        return '/'.join(url.split('/')[3:-1])
    
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
            if not os.path.exists(self.filename(url)):
                Html(url).download()
    
    def links(self):
        """查找其他链接"""
        return [tag['href'] for tag in self.soup.find(class_='x-wiki-tree')('a')]
    
    def htmlname(self, url):
        s = url.split('/')
        s = s[3:] + s[-1:]
        return '/'.join(s)
    
    def makeHtmldirs(self, url):
        """创建Html文件目录"""
        p = self.htmlPath(url)
        if p != '' and (not os.path.exists(p)):
            os.makedirs(p)
    
    def htmlPath(self, url):
        return '/'.join(url.split('/')[3:])    
    
pythonUrl = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000'
gitUrl = 'http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000'
Htmls(pythonUrl).download()
Htmls(gitUrl).download()
print 'finish'