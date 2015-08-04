from django.template import Context
from django.template.loader import render_to_string

from core.sms import InfoBip
from core.utils import replace_client_script_variables


def send_sms_birthday_greeting(client):
    if client.customer.birthday_greeting_active and client.customer.birthday_greeting_send_sms and client.phone:
        context_variables = {
            'client': client,
            'customer': client.customer,
            'message': replace_client_script_variables(client.customer.birthday_greeting_sms, client)
        }

        c = Context(context_variables)
        message = render_to_string('users/sms/birthday_greeting.txt', c).replace('\n', '')

        to = client.phone.as_e164

        sms_client = InfoBip()
        sms_client.send_sms(to, message)

        return True
    return False
