# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import hashlib
import os
import base64
import lxml
from lxml import etree
import urllib2
import json

from .models import Consumer,Account,DiningTable,ConsumeInfo,ConsumeRecord
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

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

def responseScanEvent(fromUser, toUser, content):
    responseStr="<xml><ToUserName><![CDATA[%s]]></ToUserName>\
        <FromUserName><![CDATA[%s]]></FromUserName>\
        <CreateTime>12345678</CreateTime>\
        <MsgType><![CDATA[text]]></MsgType>\
        <Content><![CDATA[%s]]></Content>\
        </xml>"%(fromUser, toUser, content)
    return responseStr



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
            #EventKey is the table index
            eventKey = xml.find("EventKey").text
            try:
                consumer = Consumer.objects.get(openId=fromUser)
            except ObjectDoesNotExist:
                consumer = Consumer.objects.create(openId=fromUser)
                account = Account.objects.create(user=consumer)
                consumer.save()
                account.save()

            if not consumer.isdining:
                consumer.isdining = True
                consumer.save()

                try:
                    table = DiningTable.objects.get(indexTable=eventKey)
                except ObjectDoesNotExist:
                    return HttpResponse(responseScanEvent(fromUser, toUser, "扫码错误!"))

                if table.status == False:
                    table.status = True

                if table.isSync == False:
                    table.status = True
                    table.save()

                cInfo, created = ConsumeInfo.objects.get_or_create(diningTable=table, status=1)
                ConsumeRecord.objects.create(consumeInfo=cInfo, consumer=consumer)

                return HttpResponse(responseScanEvent(fromUser, toUser, "欢迎入座%s号桌!"%(eventKey)))

            #consumer is in dining, get the consumeInfo
            else:
                try:
                    cRecord = ConsumeRecord.objects.get(consumer=consumer)
                except ObjectDoesNotExist:
                    return HttpResponse(responseScanEvent(fromUser, toUser, "错误状态!"))

                cInfo = cRecord.consumeInfo
                if cInfo.diningTable.indexTable == eventKey:
                    return HttpResponse(responseScanEvent(fromUser, toUser, "你已经扫过一次了!"))
                else:
                    table = DiningTable.objects.get(indexTable=eventKey)
                    cInfo.diningTable=table
                    cInfo.save()
                    return HttpResponse(responseScanEvent(fromUser, toUser, "您已换到%s号桌!"%(eventKey)))

        else:
            msgType=xml.find("MsgType").text
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
