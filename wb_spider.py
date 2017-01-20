# coding=utf-8
__author__ = 'Administrator'

# -*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import time
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
if (len(sys.argv) >= 2):
    user_id = (int)(sys.argv[1])
else:
    user_id = (int)(raw_input(u"请输入user_id: "))

cookie = {
    "Cookie": "_T_WM=f5d5a293c5de4d66c7d3c52fd5bc177e; ALF=1487410225; SCF=AgKYWDQjkoRzF68ansAXGnup7vCW0nq8KFLM9YQ1Hq_vqxzFg86RF5VuhXXtMi3CP6GE-vGluQ24qOIIP0dssJw.; SUB=_2A251hPdtDeTxGedG71YS8S_LzjuIHXVWhpklrDV6PUJbktBeLWfckW1bLa4HG5raT71I2KplG3kUqarkJQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaEwne.zfMm2zPgxAZiZxN5JpX5o2p5NHD95Qp1hBXe02pS0-NWs4DqcjeBPS0qPS0IgRReo5N; SUHB=0U1YF2ohMBukYR"}
url = 'http://weibo.cn/u/%d?page=1' % user_id

html = requests.get(url, cookies=cookie).content
selector = etree.HTML(html)
# pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
pageNum = 1
result = ""
urllist_set = set()
word_count = 1
image_count = 1
print pageNum
print u'爬虫准备就绪...'

for page in range(1, pageNum + 1):

    # 获取lxml页面
    url = 'http://weibo.cn/u/%d?page=%d' % (user_id, page)
    lxml = requests.get(url, cookies=cookie).content
    # 文字爬取
    selector = etree.HTML(lxml)
    content = selector.xpath('//span[@class="ctt"]')
    timer = selector.xpath('//span[@class="ct"]')
    for each in content:
        text = each.xpath('string(.)')
        if word_count >= 4:
            for each_timer in timer:
                timer_text = each_timer.xpath('string(.)')
                text = "%d :" % (word_count - 3) + text + timer_text + "\n\n"
                break
        else:
            text += "\n\n"
        result = result + text
        word_count += 1
    time.sleep(5)
fo = open("D:/python/project/%s" % user_id, "wb")
fo.write(result)
word_path = os.getcwd() + '/%d' % user_id
print u'文字微博爬完毕'
