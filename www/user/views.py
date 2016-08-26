# -*- coding: utf-8 -*-
# from django.db import transaction
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import logging, json
from django.http import HttpResponseRedirect
from user.models import Bind, Profile, ProfileExt,MyCollection
from logic.models import Job
from user_tools import sns_userinfo_with_userinfo, get_userid_by_openid
from common import convert, str_tools
from django.forms.models import model_to_dict


@sns_userinfo_with_userinfo
def recommand_list(request):
	return render_to_response('user/recommand_list.html')


@sns_userinfo_with_userinfo
def collection_list(request):
	user_id = get_userid_by_openid(request.openid)
	job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
	number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10
	collections = MyCollection.objects.filter(user_id=user_id).order_by('-id')[job_from_point:number_limit + job_from_point]
	job_id_list = [job.job_id for job in collections]
	collection_jobs = Job.objects.filter(id__in=job_id_list)

	user_id_list = [job.user_id for job in collection_jobs]
	profiles = Profile.objects.filter(id__in=user_id_list)

	collection_job_list = []
	user_info_map = {}
	for collection_job in collection_jobs:
		profile = profiles.get(id=collection_job.user_id)
		username = profile.real_name
		portrait = profile.portrait
		city = collection_job.city + " " + collection_job.district
		job = {'city': city, 'company_name': collection_job.company_name, 'job_title': collection_job.job_title,
		       'education': collection_job.education, 'work_experience': collection_job.work_experience, 'salary': collection_job.salary,
		       'create_time': convert.format_time(collection_job.create_time), 'username': username, 'portrait': portrait,
		       'job_uuid': collection_job.uuid, 'user_company': profile.company_name}

		user_info_map[collection_job.uuid] = convert.get_userinfo(profile)
		collection_job_list.append(job)

	if job_from_point == 0:  # 首页，需要返回页面
		page_data = {}
		page_data = {'collection_job_list': json.dumps(collection_job_list),
		             'user_info_map': json.dumps(user_info_map), 'jsapi': convert.get_jsApi(request)}
		return render_to_response('user/collection_list.html', page_data)
	else:  # 加载下一页，ajax请求
		# page_data['job_list'] = json.dumps(job_list)
		# page_data['own_job'] = []
		return HttpResponse(json.dumps(collection_job_list), content_type='application/json')


@sns_userinfo_with_userinfo
def fabu_list(request):
	user_id = get_userid_by_openid(request.openid)
	job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
	number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10
	jobs = Job.objects.filter(user_id=user_id).order_by('-id')[job_from_point:number_limit + job_from_point]
	own_job_list = []
	vip_job_list = []
	user_info_map = {}
	profile = Profile.objects.filter(id=user_id)[0]
	username = profile.real_name
	portrait = profile.portrait
	for my_job in jobs:
		city = my_job.city + " " + my_job.district
		job = {'job_uuid': my_job.uuid, 'city': city, 'company_name': my_job.company_name,
		       'job_title': my_job.job_title, 'education': my_job.education, 'work_experience': my_job.work_experience,
		       'salary': my_job.salary, 'create_time': convert.format_time(my_job.create_time), 'username': username,
		       'portrait': portrait, 'user_company': profile.company_name}
		own_job_list.append(job)
		user_info_map[my_job.uuid] = convert.get_userinfo(profile)

	if job_from_point == 0:  # 首页，需要返回页面
		page_data = {}
		page_data = {'own_job_list': json.dumps(own_job_list), 'vip_job_list': json.dumps(vip_job_list),
		             'user_info_map': json.dumps(user_info_map), 'jsapi': convert.get_jsApi(request)}
		return render_to_response('user/fabu_list.html', page_data)
	else:  # 加载下一页，ajax请求
		# page_data['job_list'] = json.dumps(job_list)
		# page_data['own_job'] = []
		return HttpResponse(json.dumps(own_job_list), content_type='application/json')


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
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	user_info_map = {}
	job_uuid = request.GET.get('job_uuid', '')
	job_detail = Job.objects.filter(uuid=job_uuid)[0]

	if job_detail:
		page_data = model_to_dict(job_detail, exclude=['id', 'user_id', 'create_time', 'update_time', ])
		page_data['city'] = job_detail.city + " " + job_detail.district
		profile = Profile.objects.filter(id=job_detail.user_id)[0]
		page_data['portrait'] = profile.portrait
		page_data['username'] = profile.real_name
		page_data['user_company'] = profile.company_name
		user_info_map[page_data['uuid']] = convert.get_userinfo(profile)

	else:
		logging.error("uid(%s) try to get not exsit job(%s), maybe attack" % (user_id, job_uuid))
		return HttpResponse("十分抱歉，获取职位信息失败，请重试。重试失败请联系客服人员")

	page_data['user_info_map'] = json.dumps(user_info_map)
	page_data['jsapi'] = convert.get_jsApi(request)
	return render_to_response('user/fabu_detail.html', page_data)  # 暂时规避跨站攻击保护


@sns_userinfo_with_userinfo
def yingpin_detail(request):
	return render_to_response('chat/chat.html')


@sns_userinfo_with_userinfo
def edit_userinfo(request):
	user_id = get_userid_by_openid(request.openid)
	profiles = Profile.objects.filter(id=user_id)[:1]
	profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
	if not profiles or not profile_exts:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")

	info = {'title': '编辑信息', 'tint': '真实信息，有利于相互信任！'}
	profile = profiles[0]
	info['real_name'] = profile.real_name
	info['company_name'] = profile.company_name
	info['user_title'] = profile.title
	info['desc'] = profile.desc

	info['city'] = profile.province + " " + profile.city + " " + profile.district

	page_data = {'info': json.dumps(info), 'jsapi': convert.get_jsApi(request)}

	return render_to_response('user/edit_userinfo.html', page_data)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@sns_userinfo_with_userinfo
def post_userinfo(request):
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	company_name = request.POST.get('company_name')
	desc = request.POST.get('jianli')
	title = request.POST.get('title')
	real_name = request.POST.get('real_name')
	addrs = request.POST.get('city').split(" ")
	province = addrs[0]
	city = addrs[1]
	district = ""
	if len(addrs) == 3:
		district = addrs[2]

	# 更新profile表 ,更新两个表应该用事务，这里暂时放下
	profiles = Profile.objects.filter(id=user_id)[:1]
	if not profiles:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")

	profile = profiles[0]
	profile.real_name = real_name
	profile.company_name = company_name
	profile.title = title
	profile.desc = desc
	profile.province = province
	profile.city = city
	profile.district = district
	profile.save()
	return HttpResponseRedirect('/user/me')


@sns_userinfo_with_userinfo
def me(request):
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	profiles = Profile.objects.filter(id=user_id)[:1]
	if not profiles:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")

	profile = profiles[0]
	if profile.real_name == '':
		info = {'title': '完善资料', 'tint': '请先完善您的资料吧！'}
		return render_to_response('user/edit_userinfo.html', {'info': json.dumps(info)})
	user_info_map = convert.get_userinfo(profile)
	# user = {'nick': profile.real_name, 'portrait': profile.portrait, 'user_company': profile.company_name,
	# 'user_title': profile.title, 'user_city': user_city, 'user_desc': profile.desc}
	page_data = {'user_info_map': json.dumps(user_info_map), 'jsapi': convert.get_jsApi(request)}
	return render_to_response('user/me.html', page_data)


@csrf_exempt
@sns_userinfo_with_userinfo
def ajax_toggle_job(request):
	user_id = get_userid_by_openid(request.openid)
	is_valid = request.POST.get('is_valid')
	job_uuid = request.POST.get('job_uuid', '')
	print is_valid
	job_detail = Job.objects.filter(uuid=job_uuid)
	data = {}
	data['status'] = "error"
	if job_detail:
		job_detail = job_detail[0]
		if is_valid == '1':  # 有效改为无效
			data['status'] = "ok"
			data['valid'] = '0'
			job_detail.is_valid = False
			job_detail.save()
		else:  # 无效改为有效
			data['status'] = "ok"
			data['valid'] = '1'
			job_detail.is_valid = True
			job_detail.save()
	else:
		logging.error("uid(%s) try to get not exsit job(%s), maybe attack" % (user_id, job_uuid))
	return HttpResponse(json.dumps(data), content_type='application/json')
