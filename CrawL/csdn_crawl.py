#!/usr/bin/env python
#coding=utf-8

import urllib
import urllib2
from lxml import etree

headers = {'Accept-Encoding': "gzip, deflate ,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Host': 'passport.csdn.net',
            }

login_data = {'_eventId': 'submit',
 'execution': 'e1s1',
 'lt': 'LT-390253-cV1c9aYHlen0TKqf7Eex4sSWwipVa0',
 'password': 'Firstlove0929',
 'username': 'furycavalier235@163.com'}



login_url = 'https://passport.csdn.net/account/login'

def get_Html(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response.read()
def get_data(url):
    tree = etree.HTML(get_Html)
    element = tree.xpath('//input')
playload = urllib.urlencode(login_data)
request = urllib2.Request(login_url, playload, headers)
response = urllib2.urlopen(request)

    
print response.read().decode('gb2312').encode('utf-8')

