# -*-coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import django.utils.timezone as timezone

class Admin_bonus(models.Model):
    create_time = models.DateTimeField()
    valid_time = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])

    def __unicode__(self):
            return "admin bonus"

class Good(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(default=0.0)
    deductible = models.BooleanField(default=True)

    def __unicode__(self):
            return self.name

class Bonus_content(models.Model):
    admin_bonus = models.ForeignKey(Admin_bonus)
    good = models.ForeignKey(Good)
    quantity = models.IntegerField(default=0)
    left_quantity = models.IntegerField(default=0)

class Consumer(models.Model):
    openId = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    sex = models.BooleanField(default=True)
    phoneNum = models.CharField(max_length=20, null=True, blank=True)
    idVIP = models.CharField(max_length=20, null=True, blank=True)
    isdining = models.BooleanField("正在就餐", default=False)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.openId

class DiningTable(models.Model):
    indexTable = models.IntegerField(primary_key=True)
    status = models.BooleanField(default=False)
    seats = models.IntegerField(default=4)
    isPrivate = models.BooleanField(default=False)
    isSync = models.BooleanField(default=False)

    def __unicode__(self):
            return "table %d"%(self.indexTable)

class ConsumeInfo(models.Model):
    totalPrice = models.IntegerField(default=0.0)
    consumerCount = models.IntegerField(default=0)
    startTime = models.DateTimeField(auto_now=True)
    finishTime = models.DateTimeField(null=True, blank=True)
    whoPay = models.CharField(null=True, blank=True, max_length=30)
    diningTable = models.ForeignKey(DiningTable, on_delete=models.CASCADE)
    status = models.IntegerField(default=1) # 1-busy 0-finished

    def __unicode__(self):
            return "table %d's ConsumeInfo"%(self.diningTable.indexTable)

class ConsumeRecord(models.Model):
    consumeInfo = models.ForeignKey(ConsumeInfo, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)

class Account(models.Model):
    sendBonusSum = models.IntegerField(default=0)
    recvBonusSum = models.IntegerField(default=0)
    totalPrice = models.FloatField(default=0.0)
    user = models.OneToOneField(Consumer, on_delete=models.CASCADE)

class SndBonus(models.Model):
    toUser = models.CharField(max_length=30)
    createTime = models.DateTimeField()
    validTime = models.DateTimeField()
    toMessage = models.CharField(max_length=45)
    fromMessage = models.CharField(max_length=45)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class RcvBonus(models.Model):
    fromUser = models.CharField(max_length=30)
    rcvTime = models.DateTimeField()
    validTime = models.DateTimeField()
    fromMessage = models.CharField(max_length=45)
    toMessage = models.CharField(max_length=45)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    consume = models.ForeignKey(ConsumeInfo, on_delete=models.CASCADE)

class AccountContent(models.Model):
    goodsNum = models.IntegerField()
    createTime = models.DateTimeField()
    validTime = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

class SndBonusContent(models.Model):
    contentNum = models.IntegerField()
    sndPackage = models.ForeignKey(SndBonus, on_delete=models.CASCADE)
    good = models.OneToOneField(Good, on_delete=models.CASCADE)

class RcvBonusContent(models.Model):
    contentNum = models.IntegerField()
    rcvPackage = models.ForeignKey(RcvBonus, on_delete=models.CASCADE)
    good = models.OneToOneField(Good, on_delete=models.CASCADE)



