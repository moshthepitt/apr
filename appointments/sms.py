from django.template import Context
from django.template.loader import render_to_string

from core.sms import InfoBip
from core.utils import replace_script_variables


def send_sms_reminder(appointment):

    context_variables = {
        'appointment': appointment,
        'customer': appointment.customer,
        'client': appointment.client,
        'event': appointment.event
    }

    if appointment.venue.custom_reminder:
        context_variables['message'] = replace_script_variables(appointment.venue.reminder_sms, appointment)
        c = Context(context_variables)
        message = render_to_string('appointments/sms/custom_reminder.txt', c).replace('\n', '')
    elif appointment.customer.custom_reminder:
        context_variables['message'] = replace_script_variables(appointment.customer.reminder_sms, appointment)
        c = Context(context_variables)
        message = render_to_string('appointments/sms/custom_reminder.txt', c).replace('\n', '')
    else:
        c = Context(context_variables)
        message = render_to_string('appointments/sms/reminder.txt', c).replace('\n', '')

    to = appointment.client.phone.as_e164

    sms_client = InfoBip()
    sms_client.send_sms(to, message)
