#coding=utf8
import hmac
import json

from settings import REDIS_WEIXIN
from .. import WeixinHelper, class_property

class CommonHelper(object):

    redis_clt = None

    def get_redis():
        if not redis_clt:
            redis_clt = redis.StrictRedis(host=REDIS_WEIXIN[0], port=REDIS_WEIXIN[1], db=REDIS_WEIXIN[2])
            return redis_clt

        # old connection, check it  缺乏redis异常处理流程
        # if not redis_clt.ping():
        #    redis_clt = redis.StrictRedis(host='localhost', port=6379, db=0) 

        return redis_clt


    @class_property
    def expire(cls):
        """比真实过期减少时间2分钟"""
        return 120


    @class_property
    def access_token_key(cls):
        return "WEIXIN_ACCESS_TOKEN"


    @class_property
    def jsapi_ticket_key(cls):
        return "WEIXIN_JSAPI_TICKET"


    @class_property
    def access_token(cls):
        cache = get_redis()
        key = cls.access_token_key
        token = cache.get(key)
        if not token:
            data = json.loads(WeixinHelper.getAccessToken())
            token, expire = data["access_token"], data["expires_in"]
            cache.set(key, token, expire-cls.expire)
        return token


    @class_property
    def jsapi_ticket(cls):
        cache = get_redis()
        key = cls.jsapi_ticket_key
        ticket = cache.get(key)
        if not ticket:
            data = json.loads(WeixinHelper.getJsapiTicket(cls.access_token))
            ticket, expire = data["ticket"], data["expires_in"]
            cache.set(key, ticket, expire-cls.expire)
        return ticket


    @classmethod
    def send_text_message(cls, openid, message):
        """客服主动推送消息"""
        return WeixinHelper.sendTextMessage(openid, message, cls.access_token)


    @classmethod
    def jsapi_sign(cls, url):
        """jsapi_ticket 签名"""
        return WeixinHelper.jsapiSign(cls.jsapi_ticket, url)


    @classmethod
    def hmac_sign(cls, key):
        return hmac.new(cls.secret_key, key).hexdigest()


    @classmethod
    def sign_cookie(cls, key):
        """cookie签名"""
        return "{0}|{1}".format(key, cls.hmac_sign(key))


    @classmethod
    def check_cookie(cls, value):
        """验证cookie
        成功返回True, key
        """
        code = value.split("|", 1)
        if len(code) != 2:
            return False, None
        key, signature = code
        if cls.hmac_sign(key) != signature:
            return False, None
        return True, key





