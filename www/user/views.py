# -*- coding: utf-8 -*-
# from django.db import transaction
from django.shortcuts import render, render_to_response

import logging
import datetime
from django.http import HttpResponse
from user.models import Bind, Profile, ProfileExt
from user_tools import sns_userinfo_with_userinfo

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
