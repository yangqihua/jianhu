# -*- coding: utf-8 -*-
# from django.db import transaction
from django.shortcuts import render, render_to_response

# Create your views here.

from django.http import HttpResponse
from common.string import gen_uuid

from user.models import Bind, Profile, ProfileExt

import logging
import datetime

# 用户关注公众号
def subscribe(openid, uninid):
	pass


# 用户关注公众号
def unsubscribe(openid, uninid):
	pass


# 从腾讯获取用户数据的回调, 存储到数据库中
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
			real_name='', company_name='', title='', vip='')
		profile.save()

		bind = Bind(user_id=profile.id, phone_number='', phone_number_verify_time='1972-01-01', wx_openid=openid,
			wx_openid_verify_time=datetime.datetime.now(), wx_subscribed=0, qq_openid='',
			qq_openid_verify_time='1972-01-01', weibo_openid='', weibo_openid_verify_time='1972-01-01', email='',
			email_verify_time='1972-01-01')
		bind.save()

		profileext = ProfileExt(user_id=profile.id, education='', nation=userinfo['country'], blood_type='',
			birthday='1972-01-01', certificate_no='', street='', province=userinfo['province'], city=userinfo['city'])
		profileext.save()
	else:
		logging.debug('exist userinfo: %s' % openid)


from wx_base.backends.dj import sns_userinfo_callback

sns_userinfo_with_userinfo = sns_userinfo_callback(fetch_user_info_callback)


@sns_userinfo_with_userinfo
def me(request):
	return render_to_response('user/me.html')

@sns_userinfo_with_userinfo
def recommand_list(request):
	return render_to_response('user/recommand_list.html')

@sns_userinfo_with_userinfo
def collection_list(request):
	return render_to_response('user/collection_list.html')

@sns_userinfo_with_userinfo
def fabu_list(request):
	return render_to_response('user/fabu_list.html')

@sns_userinfo_with_userinfo
def yinping_list(request):
	return render_to_response('user/yinping_list.html')


@sns_userinfo_with_userinfo
def recommand_detail(request):
	return render_to_response('user/recommand_detail.html')

@sns_userinfo_with_userinfo
def collection_detail(request):
	return render_to_response('user/collection_detail.html')

@sns_userinfo_with_userinfo
def fabu_detail(request):
	return render_to_response('user/fabu_detail.html')

@sns_userinfo_with_userinfo
def yingpin_detail(request):
	return render_to_response('chat/chat.html')

@sns_userinfo_with_userinfo
def edit_userinfo(request):
	return render_to_response('user/edit_userinfo.html')



@sns_userinfo_with_userinfo
def me(request):
	return render_to_response('user/me.html')
