# -*- coding: utf-8 -*-

from django.test import TestCase

import time
import redis

WEIXIN_REDIS_CLT = None

class TestRedis(object):

    def get_redis(self):
        global WEIXIN_REDIS_CLT
        if not WEIXIN_REDIS_CLT:
            WEIXIN_REDIS_CLT = redis.StrictRedis(host='139.196.140.181', port=6379, db=0)
            return WEIXIN_REDIS_CLT

        # old connection, check it  缺乏redis异常处理流程
        # if not redis_clt.ping():
        #    redis_clt = redis.StrictRedis(host='localhost', port=6379, db=0) 

        return WEIXIN_REDIS_CLT

if __name__ == '__main__':
    for i in range(100):
        print TestRedis().get_redis().ping()
        time.sleep(1)
