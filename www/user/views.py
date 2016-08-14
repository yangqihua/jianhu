# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response

# Create your views here.

from django.http import HttpResponse

# 用户关注公众号
def subscribe(openid, uninid):
    pass


# 用户关注公众号
def unsubscribe(openid, uninid):
    pass

# 从腾讯获取用户数据的回调, 存储到数据库中
def fetch_user_info_callback(openid, userinfo):
    print "openid: ", openid
    print "userinfo: ", userinfo

from wx_base.backends.dj import sns_userinfo_callback
sns_userinfo_with_userinfo = sns_userinfo_callback(fetch_user_info_callback)

@sns_userinfo_with_userinfo
def me(request):
	return render_to_response('user/me.html')