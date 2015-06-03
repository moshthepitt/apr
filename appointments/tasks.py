from datetime import timedelta, datetime
from django.utils import timezone

from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from schedule.models import Event
from schedule.periods import Period

from appointments.models import Appointment
from appointments.utils import send_period_reminders
from appointments.emails import send_cancel_email

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
    fro = datetime(year=t.year, month=t.month, day=t.day, hour=7,
                   tzinfo=timezone.get_current_timezone())
    to = fro + timedelta(1)
    period = Period(Event.objects.exclude(appointment=None).exclude(
        appointment__status=Appointment.NOTIFIED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = [x.event.id for x in event_objects]

    send_period_reminders(event_ids)


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="task_hour_to_reminder",
    ignore_result=True
)
def task_hour_to_reminder():
    """
    tries to send a reminder approximately one hour before an appointment
    given a time, say 7AM
    we look for appointments that are happening
    between 46 minutes and 1 hour from the given time
    in our case 7:46AM and 8AM
    if time now i6 7:45 we get fro=8:31 and to = 8:45
    we use 46 minutes to avoid cases where events happening at
    exactly *:15, *:30, *:45, or *:00 dont get multiple reminders
    """
    t = timezone.now()
    fro = t + timedelta(minutes=46)
    to = t + timedelta(hours=1)
    period = Period(Event.objects.exclude(appointment=None), fro, to)
    event_objects = period.get_occurrences()
    event_ids = [x.event.id for x in event_objects]

    send_period_reminders(event_ids)


@task(
    name="task_send_cancel_email",
    ignore_result=True
)
def task_send_cancel_email(appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    send_cancel_email(appointment)
