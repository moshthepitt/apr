from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


def send_email_reminder(appointment):
    current_site = Site.objects.get_current()
    current_site_domain = "http://" + current_site.domain

    c = Context({
        'appointment': appointment,
        'customer': appointment.customer,
        'client': appointment.client,
        'event': appointment.event,
        'current_site_domain': current_site_domain
    })

    client_email = "{name} <{email}>".format(name=appointment.client.get_full_name(), email=appointment.client.email)

    email_subject = render_to_string(
        'appointments/email/reminder_email_subject.txt', c).replace('\n', '')
    email_txt_body = render_to_string('appointments/email/reminder_email_body.txt', c)
    email_html_body = render_to_string('appointments/email/reminder_email_body.html', c)

    email_headers = {
        "X-Mailgun-Campaign-Id": "ffz23",
    }

    email = EmailMultiAlternatives(
        email_subject,  # subject
        email_txt_body,  # body
        settings.REMINDER_FROM_EMAIL,  # from
        [client_email],  # to
        # ['bcc@example.com'],  # bcc
        reply_to=[settings.REMINDER_FROM_EMAIL],
        headers=email_headers
    )
    email.attach_alternative(email_html_body, "text/html")

    return email.send(fail_silently=False)


def send_cancel_email(appointment):
    current_site = Site.objects.get_current()
    current_site_domain = "http://" + current_site.domain

    c = Context({
        'appointment': appointment,
        'customer': appointment.customer,
        'client': appointment.client,
        'event': appointment.event,
        'current_site_domain': current_site_domain
    })

    customer_email = "{name} <{email}>".format(name=appointment.customer.name, email=appointment.customer.email)

    email_subject = render_to_string(
        'appointments/email/cancel_notification_subject.txt', c).replace('\n', '')
    email_txt_body = render_to_string('appointments/email/cancel_notification_body.txt', c)
    email_html_body = render_to_string('appointments/email/cancel_notification_body.html', c)

    email_headers = {
        "X-Mailgun-Campaign-Id": "fg0ec",
    }

    email = EmailMultiAlternatives(
        email_subject,  # subject
        email_txt_body,  # body
        settings.REMINDER_FROM_EMAIL,  # from
        [customer_email],  # to
        # ['bcc@example.com'],  # bcc
        reply_to=[settings.REMINDER_FROM_EMAIL],
        headers=email_headers
    )
    email.attach_alternative(email_html_body, "text/html")

    return email.send(fail_silently=False)
