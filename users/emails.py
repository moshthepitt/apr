from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from core.utils import replace_client_script_variables


def send_email_birthday_greeting(client, mailgun_campaign_id=None):
    if client.customer.birthday_greeting_active and client.customer.birthday_greeting_send_email and client.email:
        current_site = Site.objects.get_current()
        current_site_domain = "http://" + current_site.domain

        context_variables = {
            'client': client,
            'customer': client.customer,
            'current_site_domain': current_site_domain,
            'subject': replace_client_script_variables(client.customer.birthday_greeting_subject, client),
            'message': replace_client_script_variables(client.customer.birthday_greeting_email, client)
        }

        c = Context(context_variables)

        email_subject = render_to_string(
            'users/email/birthday_greeting_email_subject.txt', c).replace('\n', '')
        email_txt_body = render_to_string('users/email/birthday_greeting_email_body.txt', c)
        email_html_body = render_to_string('users/email/birthday_greeting_email_body.html', c)

        sender_email = client.customer.birthday_greeting_sender
        sender = "{name} <{email}>".format(name=client.customer.name, email=sender_email)
        client_email = "{name} <{email}>".format(name=client.get_full_name(), email=client.email)

        email_headers = {}
        if mailgun_campaign_id:
            email_headers = {
                "X-Mailgun-Campaign-Id": mailgun_campaign_id,
            }

        email = EmailMultiAlternatives(
            email_subject,  # subject
            email_txt_body,  # body
            sender,  # from
            [client_email],  # to
            # ['bcc@example.com'],  # bcc
            reply_to=[sender],
            headers=email_headers
        )
        email.attach_alternative(email_html_body, "text/html")

        return email.send(fail_silently=False)
    return False
