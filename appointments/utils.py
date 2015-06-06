from django.conf import settings

from appointments.models import Appointment
from appointments.emails import send_email_reminder
from appointments.sms import send_reminder_sms


def send_period_reminders(event_ids, sendsms=False, turn_off_reminders=False):
    """
    takes a Period object
    uses the Period to get appointments and then send reminders
    """
    appointments = Appointment.objects.filter(event__id__in=event_ids).exclude(no_reminders=True)

    if appointments:
        for appointment in appointments:
            sent_email = False
            sent_sms = False
            if appointment.client.phone and sendsms and getattr(settings, 'SENDSMS', False):
                send_reminder_sms(appointment)
                sent_sms = True
            if appointment.client.email:
                send_email_reminder(appointment)
                sent_email = True
            if True in [sent_email, sent_sms]:
                if turn_off_reminders:
                    appointment.no_reminders = True
                    appointment.save()
                if appointment.status != Appointment.CONFIRMED and appointment.status != Appointment.CANCELED:
                    appointment.status = Appointment.NOTIFIED
                    appointment.save()
