from datetime import timedelta, datetime
from django.utils import timezone

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from schedule.models import Event
from schedule.periods import Period

from appointments.models import Appointment
from appointments.emails import send_email_reminder

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute=0, hour=7)),
    name="task_morning_reminders",
    ignore_result=True
)
def task_morning_reminders():
    """
    Sends a reminder to all the UN-NOTIFIED appointments
    currently sends at 7am
    """
    t = timezone.now().date()
    fro = datetime(year=t.year, month=t.month, day=t.day, hour=7, tzinfo=timezone.get_current_timezone())
    to = fro + timedelta(1)

    period = Period(Event.objects.exclude(appointment=None).exclude(appointment__status=Appointment.NOTIFIED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = [x.event.id for x in event_objects]
    appointments = Appointment.objects.filter(event__id__in=event_ids)

    if appointments:
        for appointment in appointments:
            if appointment.client.email:
                send_email_reminder(appointment)
                if appointment.status != Appointment.CONFIRMED and appointment.status != Appointment.CANCELED:
                    appointment.status = Appointment.NOTIFIED
                    appointment.save()
