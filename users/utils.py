from django.utils import timezone
from django.db.models import Count

from appointments.models import Appointment
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
                    send_email_birthday_greeting(client, mailgun_campaign_id="fr06g")
                if client.customer.birthday_greeting_send_sms:
                    send_sms_birthday_greeting(client)
    return


def clean_clients():
    """
    Try to get rid of duplicate clients by making sure only one clients with uniqu client IDs exist
    {'pk__count': 103, 'client_id': u''}
    """
    values = Client.objects.values('client_id').annotate(Count('pk')).filter(pk__count__gt=1)
    for val in values:
        if val['client_id'] and val['pk__count'] > 1:
            clients = Client.objects.filter(client_id=val['client_id'])
            if clients.count() > 1:
                main_client = clients.first()
                the_rest = clients[1:]
                appointments = Appointment.objects.filter(client__id=the_rest)
                appointments.update(client=main_client)
                the_rest.delete()

