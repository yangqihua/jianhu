# -*- coding: utf-8 -*-
import json, time
from wx_base import WxPayConf_pub
from user.models import Bind, Profile, ProfileExt
from wx_base.backends.dj import Helper
from django.http import HttpResponse

def str_to_int(str, default=0):
	try:
		return int(str)
	except Exception, e:
		return default


resource_url_base = "http://res.jianhu.com"


def get_resource_url():
	pass


def format_time(time_data):
	ts = int(time.mktime(time_data.timetuple()))
	delta = int(time.time()) - ts
	years = delta / (3600 * 24 * 365)
	months = delta / (3600 * 24 * 30)
	days = delta / (3600 * 24)
	hours = delta / 3600
	minis = delta / 60
	seconds = delta
	if years >= 1:
		return '%d年前' % years

	elif months >= 1:
		return '%d个月前' % months

	elif days >= 1:
		return '%d天前' % days

	elif hours >= 1:
		return "%d小时前" % hours

	elif minis >= 1:
		return "%d分钟前" % minis

	else:
		return "%d秒前" % seconds


def get_jsApi(request):
	url = "http://" + request.get_host() + request.get_full_path()
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID
	return json.dumps(sign)


def get_userinfo(profile):
	userinfo = {}
	userinfo['nick'] = profile.real_name
	userinfo['portrait'] = profile.portrait
	userinfo['user_company'] = profile.company_name
	userinfo['user_title'] = profile.title
	userinfo['user_desc'] = profile.desc

	userinfo['user_city'] = profile.city
	return userinfo


if __name__ == '__main__':
	print "Test str_to_int: ", str_to_int("123")
	print "Test str_to_int: ", str_to_int("123", 1)
	print "Test str_to_int: ", str_to_int("a123")
	print "Test str_to_int: ", str_to_int("a123", 1)
	print format_time("2016-08-18 16:18:31")
