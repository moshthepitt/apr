from django.conf import settings

from core.tumasms import Tumasms

tumasms = Tumasms(settings.TUMASMS_KEY, settings.TUMASMS_SIGNATURE)


def get_tumasms_balance():
    tumasms.get_balance()
    return tumasms.message()


def send_tumasms(to, message, sender_id="Vipepeo"):
    if get_tumasms_balance():
        tumasms.queue_sms(to, message, sender_id)
        tumasms.send_sms()
        return tumasms.status
    return False
