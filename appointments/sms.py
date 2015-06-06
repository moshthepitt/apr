from django.template import Context
from django.template.loader import render_to_string

from core.sms import send_sms


def send_sms_reminder(appointment):
    c = Context({
        'appointment': appointment,
        'customer': appointment.customer,
        'client': appointment.client,
        'event': appointment.event,
    })

    to = appointment.client.phone
    message = render_to_string('appointments/sms/reminder.txt', c).replace('\n', '')

    send_sms(to, message)
