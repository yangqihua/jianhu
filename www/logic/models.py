# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from user.models import Profile

# Create your models here.

class Job(models.Model):
    uuid = models.CharField(max_length=36, db_index=True)
    user_id = models.IntegerField(db_index=True)
    company_name = models.CharField(max_length=20)
    job_title = models.CharField(max_length=20)
    work_experience = models.CharField(max_length=10)
    salary = models.CharField(max_length=10)
    education = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    skill = models.CharField(max_length=120)
    piclist = models.CharField(max_length=256)
    is_valid = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "job"

    def __unicode__(self):
        return self.job_title


#请确定已有的会更新时间
class VipJobList(models.Model):
    job_id = models.IntegerField()
    user_id = models.IntegerField(primary_key=True)
    pub_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        db_table = "job_for_vip_list"


class Share(models.Model):
    share_uuid = models.CharField(max_length=36, db_index=True)
    from_user_id = models.IntegerField(db_index=True)
    to_user_id = models.IntegerField(db_index=True)
    job = models.ForeignKey(Job)
    last_share_id = models.IntegerField()
    sound_record_to_hr = models.CharField(max_length=40)
    sound_record_to_object = models.CharField(max_length=40)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "job_share"


class Conversation(models.Model):
    share_id = models.IntegerField(db_index=True)
    user_id = models.IntegerField()
    words = models.CharField(max_length=120)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation"


 #需求变更,这块后续再考虑是否更改
class MergeMsg(models.Model):
    user_id = models.IntegerField(db_index=True)
    from_user_id = models.IntegerField()
    conversation_id = models.IntegerField()
    payload = models.CharField(max_length=60)
    words = models.CharField(max_length=120)
    msg_type = models.CharField(choices=(('N', u'正常消息'), ('RR', u'推荐录音消息'), ('JS', u'相关工作状态变更消息'), ), max_length=2)
    update_time = models.DateTimeField(db_index=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "merge_msg"

