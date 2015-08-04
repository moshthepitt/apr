from django.utils import timezone

from users.models import Client
from users.sms import send_sms_birthday_greeting
from users.emails import send_email_birthday_greeting


def send_birthday_greetings(today=timezone.now()):
    """
    Sends birthday greetings for given date
    """
    clients = Client.objects.filter(birth_date__month=today.month).filter(birth_date__day=today.day)
    if clients:
        for client in clients:
            if client.customer.birthday_greeting_active:
                if client.customer.birthday_greeting_send_email:
                    send_email_birthday_greeting(client, mailgun_campaign_id="")
                if client.customer.birthday_greeting_send_sms:
                    send_sms_birthday_greeting(client)
    return
