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
    "Cookie": "SCF=Av3mJnE4NBa5e6XgVKv4VZwcgSEuInee_OOmscxrLGwWqQzTYTHwpnWc9B_tlFYbf8_Cc4OOrPWgLOrDFgh0CDU.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaEwne.zfMm2zPgxAZiZxN5JpX5o2p5NHD95Qp1hBXe02pS0-NWs4DqcjeBPS0qPS0IgRReo5N; SUHB=0HTwqvfFGbqUqN; _T_WM=2e46d2667a96be07d8d818bcf54c0267; SUB=_2A251ewy_DeTxGedG71YS8S_LzjuIHXVWh5T3rDV6PUJbkdAKLROhkW1Ef8nndpTwYbI0XuN2WIyx1OfMEg..; gsid_CTandWM=4uE55d871nBQuvUmJi4Oe7JMXcd"}
url = 'http://weibo.cn/u/%d' % user_id

html = requests.get(url, cookies=cookie).content
selector = etree.HTML(html)
# pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
pageNum = 1274
result = ""
urllist_set = set()
word_count = 1
image_count = 1

print u'爬虫准备就绪...'

for page in range(1, pageNum + 1):

    # 获取lxml页面
    url = 'http://weibo.cn/u/%d?page=%d' % (user_id, page)
    lxml = requests.get(url, cookies=cookie).content
    # 文字爬取
    selector = etree.HTML(lxml)
    content = selector.xpath('//span[@class="ctt"]')
    timer = selector.xpath('//span[@class="ct"]')
    print timer
    for each in content:
        text = each.xpath('string(.)')
        index = content.index(each)
        if word_count >= 4:
            if each.xpath('string(.//a)') == '全文':
                # print each.xpath('string(.//a/@href)')
                content_realUrl = each.xpath('string(.//a/@href)')
                content_url = 'http://weibo.cn/%s' % content_realUrl
                # print content_url
                content_lxml = requests.get(content_url, cookies=cookie).content
                # print content_lxml
                content_selector = etree.HTML(content_lxml)
                real_content = content_selector.xpath('//span[@class="ctt"]')
                if len(real_content):
                    text = real_content[0].xpath('string(.)')
            else:
                text = each.xpath('string(.)')
            timer_text = timer[index - 3].xpath('string(.)')
            text = "%d :" % (word_count - 3) + text + timer_text + "\n\n"
        else:
            text += "\n\n"
        result = result + text
        word_count += 1
    print "finish %d" % page
    time.sleep(2)
fo = open("/opt/weibo/%s" % user_id, "wb")
fo.write(result)
word_path = os.getcwd() + '/%d' % user_id
print u'文字微博爬完毕'
