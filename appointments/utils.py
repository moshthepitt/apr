from django.conf import settings
from django.utils import timezone

from reminders.models import Reminder

from appointments.models import Appointment
from appointments.emails import send_email_reminder
from appointments.sms import send_sms_reminder


def send_period_reminders(event_ids, sendsms=False, turn_off_reminders=False, mailgun_campaign_id=None):
    """
    takes a Period object
    uses the Period to get appointments and then send reminders
    """
    appointments = Appointment.objects.filter(event__id__in=event_ids).exclude(no_reminders=True).distinct()

    if appointments:
        for appointment in appointments:
            sent_email = False
            sent_sms = False
            if appointment.client.phone and sendsms and getattr(settings, 'SENDSMS', False):
                if appointment.customer.send_sms:
                    if appointment.venue.send_sms:
                        send_sms_reminder(appointment)
                        sent_sms = True
            if appointment.client.email:
                if appointment.customer.send_email:
                    if appointment.venue.send_email:
                        send_email_reminder(appointment, mailgun_campaign_id)
                        sent_email = True
            if True in [sent_email, sent_sms]:
                if turn_off_reminders:
                    appointment.no_reminders = True
                    appointment.save()
                if appointment.status != Appointment.CONFIRMED and appointment.status != Appointment.CANCELED:
                    appointment.status = Appointment.NOTIFIED
                    appointment.save()
                reminder = Reminder(
                    customer=appointment.customer,
                    appointment=appointment,
                    client_name=appointment.client.get_full_name(),
                    appointment_time=timezone.localtime(appointment.event.start),
                    sent_email=sent_email,
                    sent_sms=sent_sms
                )
                reminder.save()
