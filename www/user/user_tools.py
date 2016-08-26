# -*- coding: utf-8 -*-

import logging
from common.str_tools import gen_uuid
from user.models import Bind, Profile, ProfileExt
import datetime

# 用户关注公众号
def subscribe(openid, uninid):
    pass


# 用户关注公众号
def unsubscribe(openid, uninid):
    pass


# 从腾讯获取用户数据的回调, 存储到数据库中, 因为有多表，需要增加事物控制
# @transaction.commit_on_success
def fetch_user_info_callback(openid, userinfo):
    exist = Bind.objects.filter(wx_openid=openid)
    if not exist:
        logging.info("new user. openid: %s  userinfo: %s" % (openid, userinfo))
        sex = 'O'
        if 'sex' in userinfo:
            if userinfo['sex'] == 1:
                sex = 'M'
            else:
                sex = 'F'

        profile = Profile(uuid=gen_uuid(), nick=userinfo['nickname'], sex=sex, portrait=userinfo['headimgurl'],
            real_name='', company_name='', title='', vip='1', desc='', nation=userinfo['country'], province=userinfo['province'], city=userinfo['city'], district='')
        profile.save()

        bind = Bind(user_id=profile.id, phone_number='', phone_number_verify_time='1972-01-01', wx_openid=openid,
            wx_openid_verify_time=datetime.datetime.now(), qq_openid='',
            qq_openid_verify_time='1972-01-01', weibo_openid='', weibo_openid_verify_time='1972-01-01', email='',
            email_verify_time='1972-01-01')
        bind.save()

        profileext = ProfileExt(user_id=profile.id, education='', blood_type='', birthday='1972-01-01', certificate_no='')
        profileext.save()
    else:
        logging.debug('exist userinfo: %s' % openid)

from wx_base.backends.dj import sns_userinfo_callback
sns_userinfo_with_userinfo = sns_userinfo_callback(fetch_user_info_callback)

def get_userid_by_openid(openid):
    if openid:
        binds = Bind.objects.filter(wx_openid=openid).only('user_id')[:1]
        if binds:
            return binds[0].user_id

    return None

def get_user_profile_by_user_id(user_id, need_default):
    profiles = Profile.objects.filter(id=user_id)[:1]
    if profiles:
        return profiles[0]

    if need_default:
        return Profile(id=user_id, uuid='', nick='', sex='O', real_name='', portrait='', company_name='', title='', vip=False, desc='', nation='', province='', city='', district='')
    else:
        return None

def is_vip(user_id):
    profiles = Profile.objects.filter(id=user_id)[:1]
    if profiles and profiles[0].vip:
        return True

    return False
