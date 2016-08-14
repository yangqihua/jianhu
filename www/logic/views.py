# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
# Create your views here.
from common import convert
from django.http import HttpResponse
from models import Job, VipJobList

import logging
from common.string import gen_uuid

from user.views import fetch_user_info_callback
from wx_base.backends.dj import sns_userinfo_callback
sns_userinfo_with_userinfo = sns_userinfo_callback(fetch_user_info_callback)

@sns_userinfo_with_userinfo
def index(request):
	uid = 1  # get uid from session

	vip_job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
	number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10

	# 取本人发布过的，并且有效的简历
	if vip_job_from_point != 0:
		own_jobs = []
	else:
		own_jobs = Job.objects.filter(id=uid).order_by('-id')[0:1]

	# 按发布时间去取VIP发布简历 －－ 以后从缓存中取
	vip_jobs = VipJobList.objects.all()[vip_job_from_point:number_limit]
	job_id_list = [job.job_id for job in vip_jobs]

	vip_jobs = Job.objects.filter(id__in=job_id_list)

	# ready to render

	return render_to_response('index.html')

@sns_userinfo_with_userinfo
def msg(request):
	return render_to_response('chat/mesg.html')

@sns_userinfo_with_userinfo
def home(request):
	return HttpResponse("请渲染Home页")

@sns_userinfo_with_userinfo
def get_job(request):
	uid = 1  # get uid from session

	job_uuid = request.GET.get('job_uuid', '')
	job_detail = Job.objects.filter(uuid=job_uuid)[0:1]
	if job_detail:
		# 开始渲染
		pass
	else:
		logging.error("uid(%s) try to get not exsit job(%s), maybe attack" % (uid, job_uuid))
	# 返回错误

	return render_to_response('job/job_detail.html')

@sns_userinfo_with_userinfo
def post_job(request):
	company_name = request.POST.get('company_name')
	job_title = request.POST.get('job_title')
	work_experience = request.POST.get('work_experience')
	salary = request.POST.get('salary')
	education = request.POST.get('education')
	city = request.POST.get('city')
	skill = request.POST.get('skill')
	piclist = request.POST.get('piclist')

	user_id = 1  # get userid from session

	job = Job(uuid=gen_uuid(), user_id=user_id, company_name=company_name, job_title=job_title,
		work_experience=work_experience, salary=salary, education=education, city=city, skill=skill, piclist=piclist)
	job.save()

	is_vip = True

	if is_vip:
		vip_job = VipJobList(job_id=job.id)
		vip_job.save()

	return render_to_response('job/job_fabu.html')

@sns_userinfo_with_userinfo
def post_job_success(request):
	return render_to_response('job/job_success.html')

@sns_userinfo_with_userinfo
def fabu_job(request):
	return render_to_response('job/job_fabu.html')

@sns_userinfo_with_userinfo
def recommand_job(request):
	return render_to_response('job/job_recommand.html')

@sns_userinfo_with_userinfo
def chat(request):
	return render_to_response('chat/chat.html')
