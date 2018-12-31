from django.utils import timezone
from django.db.models import Count
from django.conf import settings

from appointments.models import Appointment
from users.models import Client
from users.sms import send_sms_birthday_greeting
from users.emails import send_email_birthday_greeting


def send_birthday_greetings(today=timezone.now()):
    """
    Sends birthday greetings for given date
    """
    clients = Client.objects.filter(birth_date__month=today.month).filter(
        birth_date__day=today.day)
    if clients:
        for client in clients:
            if client.customer.birthday_greeting_active:
                if client.customer.birthday_greeting_send_email:
                    send_email_birthday_greeting(
                        client, mailgun_campaign_id="fr06g")
                if client.customer.birthday_greeting_send_sms:
                    send_sms_birthday_greeting(client)
    return


def clean_clients():
    """
    Try to get rid of duplicate clients by making sure only one clients with
    unique client IDs exist
    {'pk__count': 103, 'client_id': u''}
    """
    values = Client.objects.values('client_id').annotate(
        Count('pk')).filter(pk__count__gt=1)
    for val in values:
        if val['client_id'] and val['pk__count'] > 1:
            clients = Client.objects.filter(client_id=val['client_id'])
            if clients.count() > 1:
                main_client = clients.first()
                duplicate_clients = clients[1:]
                Appointment.objects.filter(
                    client__ii=duplicate_clients).update(client=main_client)
                for duplicate_client in duplicate_clients:
                    duplicate_client.delete()


def get_client_id(client,
                  prefix=settings.APR_CLIENTID_PREFIX,
                  separator="-",
                  use_name=False):
    """
    Generate client id

    :param client: the client object
    :param prefix: the prefix to put in the client id
    :param separator: the separator to put after the prefix
    :param last_name: the last_name of the client
    :return: client_id
    """
    number = 1

    if use_name:
        name = next(
            (x for x in [client.last_name, client.first_name]), None)
        if name:
            last_client_by_name = Client.objects.filter(
                last_name__istartswith=name[0],
                customer=client.customer).order_by('-client_id').first()
            if last_client_by_name:
                curr_id = last_client_by_name.client_id
                if curr_id:
                    try:
                        number = int(filter(str.isdigit, curr_id))
                    except TypeError:
                        try:
                            number = int(filter(unicode.isdigit, curr_id))
                        except ValueError:
                            pass
                    except ValueError:
                        pass

                    return "{prefix}{initial}{separator}{number}".format(
                        prefix=prefix,
                        initial=client.last_name[0].upper(),
                        separator=separator,
                        number=number)

    return "{prefix}{separator}{number}".format(
        prefix=prefix,
        separator=separator,
        number=client.id)
