# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response

# Create your views here.

from django.http import HttpResponse

# 用户关注公众号
def subscribe(request):
    pass

# 用户授权访问
def suthorize(request):
    pass


def me(request):
	return render_to_response('user/me.html')