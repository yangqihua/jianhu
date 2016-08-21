# -*- coding: utf-8 -*-

import oss2
import requests
import logging
from settings import ALI_ACCESS_KEY, ALI_ACCESS_SECRET

# osspython sdk： https://help.aliyun.com/document_detail/32026.html?spm=5176.doc32039.6.304.J2Ctrr
# oss出错处理： https://help.aliyun.com/document_detail/32039.html?spm=5176.doc32029.6.317.yvhgR0

class OSSTools(object):

    def __init__(self, bucket_name):
        self.auth = oss2.Auth(ALI_ACCESS_KEY, ALI_ACCESS_SECRET)
        self.bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', bucket_name, connect_timeout=3)

    def upload_from_url(self, picname, url):
        #从腾讯拉取图片可能失败
        #放入oss中可能失败
        #以后要进行后台检查，检查失败率
        logging.error('[UploadToOSS] From %s To %s' % (url, picname))
        self.bucket.put_object(picname, requests.get(url))

