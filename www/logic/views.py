# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, RequestContext
from common import convert, str_tools
from django.http import HttpResponse,HttpResponseRedirect
from models import Job, VipJobList
import json
import oss2
import logging
import requests
from wx_base.backends.common import CommonHelper
from settings import ALI_ACCESS_KEY, ALI_ACCESS_SECRET
from wx_base.backends.dj import Helper, sns_userinfo
from wx_base import WeixinHelper, JsApi_pub, WxPayConf_pub, UnifiedOrder_pub, Notify_pub, catch
from user.user_tools import sns_userinfo_with_userinfo, get_userid_by_openid, is_vip


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

	url = "http://" + request.get_host() + request.path
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID

	return render_to_response('job/job_detail.html', {"jsapi": json.dumps(sign)})


#暂时规避跨站攻击保护
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@sns_userinfo_with_userinfo
def post_job(request):
	company_name = request.POST.get('company_name')
	job_title = request.POST.get('job_title')
	work_experience = request.POST.get('work_experience')
	salary = request.POST.get('salary')
	education = request.POST.get('education')
	city = request.POST.get('city')

	skill = request.POST.get('skill1') + "," + request.POST.get('skill2') + "," + request.POST.get(
		'skill3') + "," + request.POST.get('skill4') + "," + request.POST.get('skill5') + "," + request.POST.get(
		'skill6')

	piclist = ''

	auth = oss2.Auth(ALI_ACCESS_KEY, ALI_ACCESS_SECRET)
	bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'ugcres')
	access_token = CommonHelper.access_token()
	for i in range(1, 7):
		media_id = request.POST.get('img_url%s' % i)
		if media_id:
			url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (access_token, media_id)
			picname = str_tools.gen_short_uuid()
			bucket.put_object(picname, requests.get(url))
			if piclist:
				piclist = '%s,%s' % (piclist, picname)
			else:
				piclist = picname

	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return "异常页面, 需要界面"

	job = Job(uuid=str_tools.gen_uuid(), user_id=user_id, company_name=company_name, job_title=job_title,
		work_experience=work_experience, salary=salary, education=education, city=city, skill=skill, piclist=piclist)
	job.save()

	if is_vip(user_id):
		vip_job = VipJobList(job_id=job.id, user_id=user_id)
		vip_job.save()

	url = "http://" + request.get_host() + request.path
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID
	return render_to_response('job/job_success.html', {"jsapi": json.dumps(sign)})


@sns_userinfo_with_userinfo
def fabu_job(request):
	url = "http://" + request.get_host() + request.path
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID
	return render_to_response('job/job_fabu.html', {"jsapi": json.dumps(sign)})


@sns_userinfo_with_userinfo
def recommand_job(request):
	return render_to_response('job/job_recommand.html')


@sns_userinfo_with_userinfo
def chat(request):
	return render_to_response('chat/chat.html')
