# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from common import convert
from django.http import HttpResponse
from models import Job,VipJobList

import uuid
import logging

#暂时忽略权限问题
def index(request):

    uid = 1 #get uid from session

    vip_job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0) #有from时，则为翻页，无时，则为首页
    number_limit = convert.str_to_int(request.GET.get('limit', '5'), 5) #异常情况下，或者不传的情况下，默认为5

    #取本人发布过的，并且有效的简历
    if vip_job_from_point != 0:
        own_jobs = []
    else:
        own_jobs = Job.objects.filter(id=uid).order_by('-id')[0:5]

    #按发布时间去取VIP发布简历 －－ 以后从缓存中取
    vip_jobs = VipJobList.objects.all()[0:10]
    job_id_list = [job.job_id for job in vip_jobs]

    vip_jobs = Job.objects.filter(id__in=job_id_list)

    #ready to render

    return HttpResponse("可以开始渲染了")

def get_job(request):

    uid = 1 #get uid from session

    job_uuid = request.GET.get('job_uuid', '')
    job_detail = Job.objects.filter(uuid=job_uuid)[0:1]
    if job_detail:
        #开始渲染
        pass
    else:
        logging.error("uid(%s) try to get not exsit job(%s), maybe attack" % (uid, job_uuid))
        #返回错误
    
    return HttpResponse("可以开始渲染了")

def post_job(request):

    company_name = request.POST.get('company_name')
    job_title = request.POST.get('job_title')
    work_experience = request.POST.get('work_experience')
    salary = request.POST.get('salary')
    education = request.POST.get('education')
    city = request.POST.get('city')
    skill = request.POST.get('skill')
    piclist = request.POST.get('piclist')

    user_id = 1 #get userid from session
    uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'jianhu-www')

    job = Job(uuid=uuid,user_id=user_id,company_name=company_name,job_title=job_title,work_experience=work_experience,salary=salary,education=education,city=city,skill=skill,piclist=piclist)
    job.save()

    is_vip = True

    if is_vip:
        vip_job = VipJobList(job_id=job.id)
        vip_job.save()

    return HttpResponse("可以开始渲染了")
