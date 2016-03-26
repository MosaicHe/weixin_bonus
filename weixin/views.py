#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import hashlib
import os
import base64
import lxml
from lxml import etree
import urllib2
import json

global open_id
open_id = "none"

global appid
global appsecret
appid="wx755ab5b9ed026b96"
appsecret="067d1268812a33d924bc88168d4edd08"

def get_openid(request):
    code=request.GET.get(u'code') 
    print("*************************test******************************")
    response = urllib2.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appid,appsecret,code))     
    content = response.read()
    s=json.loads(content)
    return HttpResponse("Hello, %s"%s["openid"])


def get_userinfo(request):
    code=request.GET.get(u'code') 
    print("*************************test******************************")
    response = urllib2.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appid,appsecret,code))     
    content = response.read()
    s=json.loads(content)
    access_token=s["access_token"]
    openid=s["openid"]
    response = urllib2.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN'%(access_token,openid))     
    content = response.read()
    print(content)
    return HttpResponse(content)
    
def index(request):
    global open_id
    print("*************************index******************************")
    #snsapi_base only get openid,need not user auth
    #return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx755ab5b9ed026b96&redirect_uri=http://ec2-54-249-46-10.ap-northeast-1.compute.amazonaws.com/weixin/get_openid&response_type=code&scope=snsapi_base&state=1#wechat_redirect")

    #snsapi_userinfo,get user information, need user auth
    return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx755ab5b9ed026b96&redirect_uri=http://ec2-54-249-46-10.ap-northeast-1.compute.amazonaws.com/weixin/get_userinfo&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect")
    #return HttpResponse("Hello, %s"%open_id)

@csrf_exempt
def token(request):
    global open_id
    print("*************************token******************************")
    #获取输入参数
    #print(request.META)
    if(request.method=="GET"):
        print(request.GET)
        signature=request.GET.get(u'signature')
        timestamp=request.GET.get(u'timesamp')
        nonce=request.GET.get(u'nonce')
        echostr=request.GET.get(u'echostr')
        return HttpResponse(echostr) 

    elif(request.method == "POST"):
        
        print(request.body)
        xml = etree.fromstring(request.body)#进行XML解析
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if(xml.find('Event').text=="SCAN"):
            responeStr="<xml><ToUserName><![CDATA[%s]]></ToUserName>\
                            <FromUserName><![CDATA[%s]]></FromUserName>\
                            <CreateTime>12345678</CreateTime>\
                            <MsgType><![CDATA[text]]></MsgType>\
                            <Content><![CDATA[你好]]></Content>\
                            </xml>"%(fromUser, toUser)
            return HttpResponse(responeStr) 
        else:
            msgType=xml.find("MsgType").text
            open_id=fromUser
            return HttpResponse("hero") 

    '''
    #自己的token
    token="token" #这里改写你在微信公众平台里输入的token
    #字典序排序
    #list=[token,timestamp,nonce]
    #list.sort()
    #sha1=hashlib.sha1()
    #map(sha1.update,list)
    #hashcode=sha1.hexdigest()
    #sha1加密算法        

    #如果是来自微信的请求，则回复echostr
    if hashcode == signature:
        return HttpResponse(echostr) 
    else:
        return HttpResponse(echostr) 
'''
