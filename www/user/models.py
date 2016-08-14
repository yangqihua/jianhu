# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Profile(models.Model):
    #####################################
    uuid = models.CharField(max_length=36, db_index=True)
    nick = models.CharField(max_length=20)
    sex = models.CharField(choices=(('F', 'Female'), ('M', 'Male'), ('O', 'Other')), max_length=1)
    portrait = models.CharField(max_length=20)
    real_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    vip = models.BooleanField(default=False)
    ################# 以上是概要信息部分 #####
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_profile"

    def __unicode__(self):
        return self.nick


class ProfileExt(models.Model):
    user_id = models.IntegerField(db_index=True)
    education = models.CharField(max_length=40)
    nation = models.CharField(max_length=20)
    blood_type = models.CharField(max_length=3)
    birthday = models.DateField()
    certificate_no = models.CharField(max_length=40)
    street = models.CharField(max_length=40)
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_profile_ext"


class Bind(models.Model):
    user_id = models.IntegerField(db_index=True)
    phone_number = models.CharField(max_length=20, db_index=True)
    phone_number_verify_time = models.DateTimeField()
    wx_openid = models.CharField(max_length=20, db_index=True)
    wx_openid_verify_time = models.DateTimeField() #如果只是授权没有关注，则该值为0000-00-00，订阅状态为false；如果是取消关注，则该值为注册时间，未关注
    wx_subscribed = models.BooleanField(default=False)
    qq_openid = models.CharField(max_length=20, db_index=True)
    qq_openid_verify_time = models.DateTimeField()
    weibo_openid = models.CharField(max_length=20, db_index=True)
    weibo_openid_verify_time = models.DateTimeField()
    email = models.CharField(max_length=40, db_index=True)
    email_verify_time = models.DateTimeField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_bind"


class MyCollection(models.Model):
    user_id = models.IntegerField(db_index=True)
    job_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "my_collection"


class MyRecommend(models.Model):
    user_id = models.IntegerField(db_index=True)
    job_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "my_recommend"


class MyInterview(models.Model):
    user_id = models.IntegerField(db_index=True)
    job_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "my_interview"
