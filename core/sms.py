from django.conf import settings

from oneapi import SmsClient, CustomerProfileClient
from oneapi.models import SMSRequest
from core.tumasms import Tumasms


def tumasms_get_balance():
    tumasms = Tumasms(settings.TUMASMS_KEY, settings.TUMASMS_SIGNATURE)
    tumasms.get_balance()
    return tumasms.message()


def tumasms_send_sms(to, message, sender_id="Vipepeo"):
    if tumasms_get_balance() > 0:
        tumasms = Tumasms(settings.TUMASMS_KEY, settings.TUMASMS_SIGNATURE)
        tumasms.queue_sms(to, message, sender_id, "")
        tumasms.send_sms()
        return True
    return False


class InfoBip(object):
    username = settings.INFOBIP_USERNAME
    password = settings.INFOBIP_PASSWORD

    def get_balance(self):
        profile = CustomerProfileClient(self.username, self.password)
        balance = profile.get_account_balance()
        return balance.balance

    def send_sms(self, to, message):
        if self.get_balance > 0:
            client = SmsClient(self.username, self.password)
            sms = SMSRequest()
            sms.sender_address = "appointware"
            sms.address = to
            sms.message = message
            sms.callback_data = ''
            client.send_sms(sms)
