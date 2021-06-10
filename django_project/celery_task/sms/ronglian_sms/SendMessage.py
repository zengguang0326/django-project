import json

from celery_task.sms.ronglian_sms import SmsSDK

_accId = '8a216da878005a80017802e4f9f501b8'
_accToken = '9e506cd80f6145e7b5356b8d647198b8'
_appId = '8a216da878005a80017802e4fafc01bf'


class SMS(object):

    def __new__(cls,*args,**kwargs):
        # 如果 SMS类没有已经创建好的对象则创建一个，有的话直接返回
        # if cls.instance is None:
        if not hasattr(SMS,'_instance'):
            cls._instance = super(SMS,cls).__new__(cls, *args, **kwargs)
            cls._instance.sdk = SmsSDK(_accId, _accToken, _appId)
        return cls._instance

    def send_message(self,tid, mobile, datas):

        resp = self.sdk.sendMessage(tid, mobile, datas)
        # print(type(resp))
        status_code = json.loads(resp).get("statusCode")
        if status_code == "000000":
        #     发送成功返回0
            return 0
        else:
        #     失败返回-1
            return -1

# print(id(send_message()))
# print(id(send_message()))
# sdk =
# tid = '1'
# mobile = '15922071727'
# datas = ('5432', '5')
# sms=SMS()
# rs=sms.send_message(tid,mobile,datas)
# print(rs)
#
# print(SMS())
# print(SMS())