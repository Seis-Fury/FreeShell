#/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created by Fury 2017/08/14
登录CSDN成功
测试使用cookie失败
在提交的表单里添加 rememberMe:true 再次测试，成功
'''

import requests
from lxml import etree
import sys
import http.cookiejar

headers = {'Accept-Encoding': "gzip, deflate ,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Host': 'passport.csdn.net',
            'Content-type': 'application/x-www-form-urlencoded',
            }

def get_url(url):
    req = requests.get(url)
    if req.status_code == 200:
        #print 'Do
        #fp  = open('./Html/douban.html','w')
        #fp.writelines(req.content)
        return req.content
    else:
        print 'Disconnect'
def get_data(content):
    data = {'_eventId': 'submit',
    'password': 'nocrying_0207',
    'username': 'furycavalier235@163.com',
    'rememberMe':'true',
    }
    tree = etree.HTML(content)
    lt = tree.xpath('//input[@name="lt"]/@value')[0]
    _execution = tree.xpath('//input[@name="execution"]/@value')[0]
    data['lt'] = lt
    data['execution'] = _execution

    return data

def test_xrsl():
    path = './Html/douban.html'
    content = open(path).read()
    tree = etree.HTML(content)
    input_list = tree.xpath('//input')
    for each in input_list:
        name = each.xpath('./@name')
        value = each.xpath('./@value')
        print name
        print value

def test_cookie():
    
    _file = './Html/csdn.cookie'
    url = 'http://my.csdn.net/'
    #创建LWPCookieJar的实例
    cj = http.cookiejar.LWPCookieJar()
    #加载cookies
    cj.load(_file, ignore_discard=True)
    #将cookiejar类转化成字典
    cookie_load = requests.utils.dict_from_cookiejar(cj)
    #创建session
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookie_load)
    #使用cookie后并未成功 
    r = session.get(url,headers=headers)
    print r.content

    r = requests.get(url,headers=headers,cookies=cookie_load)
    print r.content
    


def main():
    url = 'https://passport.csdn.net/account/login'
    #print get_data(url)
    refer_url =  'http://my.csdn.net/'
    session = requests.session()

    #generate cookies
    filename = './Html/csdn.cookie'
    session.cookies = http.cookiejar.LWPCookieJar(filename)
    req = session.get(url,headers=headers)
    

    data = get_data(req.content)
    #print data
    res = session.post(url,data=data,headers=headers)
    print res.content
    session.cookies.save()

    result = session.get(refer_url, headers = headers)
    print result.content
if __name__ == '__main__':
    #main()
    test_cookie()
