# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Profile(models.Model):
    #####################################
    uuid = models.CharField(max_length=40)
    name = models.CharField(max_length=20)
    nick = models.CharField(max_length=20)
    sex = models.CharField(choices=(('F', 'Female'), ('M', 'Male'), ('O', 'Other')), max_length=1)
    portrait = models.CharField(max_length=40)
    #################以上是概要信息部分#####
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

class ProfileExt(models.Model):
    user = models.ForeignKey(Profile)
    education = models.CharField(max_length=40)
    nation = models.CharField(max_length=20)
    blood_type = models.CharField(max_length=3)
    birthday = models.DateField()
    certificate_no = models.CharField(max_length=40)
    street = models.CharField(max_length=40)
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

class Bind(models.Model):
    user = models.ForeignKey(Profile)
    phone_number = models.CharField(max_length=20)
    phone_number_verify_time = models.DateTimeField()
    wx_openid = models.CharField(max_length=20)
    wx_openid_verify_time = models.DateTimeField()
    qq_openid = models.CharField(max_length=20)
    qq_openid_verify_time = models.DateTimeField()
    weibo_openid = models.CharField(max_length=20)
    weibo_openid_verify_time = models.DateTimeField()
    email = models.CharField(max_length=40)
    email_verify_time = models.DateTimeField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

#
# type ShareAction struct {
# 	ShareId     int64
# 	TopicId     int64
# 	PreUserId   int64
# 	NextUserId  int64
# 	create_time string
# }
#
# type ShareCommunicate struct {
# 	ShareId     int64
# 	UserId      int64
# 	words       string
# 	create_time string
# }