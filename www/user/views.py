# -*- coding: utf-8 -*-
# from django.db import transaction
from django.shortcuts import render, render_to_response

import logging, json
from django.http import HttpResponseRedirect
from user.models import Bind, Profile, ProfileExt
from user_tools import sns_userinfo_with_userinfo, get_userid_by_openid


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
    info = {'title': '修改资料', 'tint': '请填写您的修改资料内容！'}
    return render_to_response('user/edit_userinfo.html', {'info': json.dumps(info)})


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@sns_userinfo_with_userinfo
def post_userinfo(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    company_name = request.POST.get('company_name')
    title = request.POST.get('title')
    real_name = request.POST.get('real_name')
    city = request.POST.get('city')

    # 更新profile表 ,更新两个表应该用事务，这里暂时放下
    profile = Profile.objects.filter(id=user_id)[0]
    profile.real_name = real_name
    profile.company_name = company_name
    profile.title = title
    profile.save()

    # 更新profile_ext表
    profile_ext = ProfileExt.objects.filter(user_id=user_id)[0]
    profile_ext.city = city
    profile_ext.save()
    return HttpResponseRedirect('/user/me')


@sns_userinfo_with_userinfo
def me(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    profile = Profile.objects.filter(id=user_id)[0]
    if profile.real_name == '':
        info = {'title': '完善资料', 'tint': '请先完善您的资料吧！'}
        return render_to_response('user/edit_userinfo.html', {'info': json.dumps(info)})
    else:
        city = ''
        profile_ext = ProfileExt.objects.filter(user_id=user_id)[:1]
        if profile_ext:
           city = profile_ext[0].city 

        user = {'nick': profile.real_name, 'portrait': profile.portrait, 'company': profile.company_name,
                'city': city}
        return render_to_response('user/me.html', {'user': json.dumps(user)})

