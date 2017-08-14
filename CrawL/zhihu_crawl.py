#/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import re
import subprocess
import json
import http.cookiejar

headers =  {'Accept-Encoding': "gzip, deflate ,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Host': 'www.zhihu.com',
            'Content-type': 'application/x-www-form-urlencoded',
            }
homeURL = "http://www.zhihu.com"
captchaURL = "http://www.zhihu.com/captcha.gif"
login_url = "https://www.zhihu.com/login/email"

payload = {
        'email': 'romancedawn9734@gmail.com',
        'password': 'DoubleD359',
        }

def get_xsrf(content):
    #xpath
    root = etree.HTML(content)
    XSRF = root.xpath("//input[@name='_xsrf']/@value")[0]
    #BeautifulSoup
    soup = BeautifulSoup(content,'html.parser')
    print soup.find('input',{'name':'_xsrf'})['value']
    
    return XSRF


def test_cookie1():
    #测试读取CookieJar()加载知乎主页
    url = 'http://www.zhihu.com'
    filename1 = './Html/zhihu_1.cookie' 

    session = requests.session()
    # 使用http.cookies.LWPCookieJar()生成cookie的类
    session.cookies = http.cookiejar.LWPCookieJar(filename)
    try:
        session.cookies.load(ignore_discard=True)
        req = session.get(url, headers)
        print req.content
    except:
        print '加载失败'

def test_cookie2():
    #测试读取字典类cookie加载知乎主页
    url = 'http://www.zhihu.com'
    filename = './Html/zhihu_1.cookie'
    #使用requests库获取主页，测试成功
    cj = http.cookiejar.LWPCookieJar(filename)
    cj.load(ignore_discard=True)
    cookie_dict = requests.utils.dict_from_cookiejar(cj)
    r = requests.get(url, headers=headers, cookies=cookie_dict)

    #print r.content

    #使用requests.session登录主页 和测试1的方法类似
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
    r_new = session.post(url, headers=headers)

    print r_new.content
    





def main():
    url = 'http://www.zhihu.com'
    #创建会话
    filename = './Html/zhihu_1.cookie' #使用http.cookie.LWPCookieJar()生成,测试添加headers可以直接访问知乎
    
    session = requests.session()
    # 使用http.cookies.LWPCookieJar()生成cookie的类
    #session.cookies = http.cookiejar.LWPCookieJar(filename1)
    #生成cookie

    #获取_xsrf文件
    r = session.get(url, headers=headers)
    payload['_xsrf'] = get_xsrf(r.content)
    #获取验证码
    
    #如果不去输入验证码
    #result = session.post(login_url, data=payload, headers=headers)
    #print json.loads(result.content)["msg"] #"\u9a8c\u8bc1\u7801\u4f1a\u8bdd\u65e0\u6548 :("
    #print result.content #验证码会话无效 :(
    nowtime = str(int(time.time())*1000)
    captcha_url = captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                 nowtime + "&type=login"
    cap = session.get(captcha_url, headers=headers)
    with open('check_img.gif','wb') as f:
        f.write(cap.content)
        f.close()
    subprocess.check_output(['open','check_img.gif'])
    captcha = raw_input("请输入验证码:")
    payload['captcha']=captcha
    #print cap.content

    result = session.post(login_url, data=payload, headers=headers)
    if result.json()['r'] == 1:
        nowtime = str(int(time.time())*1000)
        captcha_url = captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                 nowtime + "&type=login"
        cap = session.get(captcha_url, headers=headers)
        with open('check_img.gif','wb') as f:
            f.write(cap.content)
            f.close()
        subprocess.check_output(['open','check_img.gif'])
        captcha = raw_input("请输入验证码:")
        print captcha
        payload['captcha']=captcha

        result = session.post(login_url, data=payload, headers=headers)
        print result.json()
    else:
        item = result.json()
        #session.cookies.save()
        print item["msg"]    
if __name__ == '__main__':
    main()
    #test_cookie2()
