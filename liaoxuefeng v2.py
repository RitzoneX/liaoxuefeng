# -*- coding: utf-8 -*-

import re
from html import Html
from pprint import pprint
import logging
from multiprocessing.dummy import Pool


def down(url):
    h = Html(url)
    result = re.search(
        r'(?s)<div class="x-wiki-tree">.*?</div>', h.html).group()
    urls = re.findall(r'http://[^"]*', result)
    # for url in urls:
    #     Html(url).download()

    pool = Pool(5)
    pool.map(multiDownload, urls)
    pool.close()
    pool.join()

    h.download()


def multiDownload(url):
    """多线程方法"""
    Html(url).download()

pythonUrl = 'http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000'
gitUrl = 'http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000'

# logging.basicConfig(level=logging.DEBUG)
down(pythonUrl)
down(gitUrl)
