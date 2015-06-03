from datetime import timedelta, datetime
from django.utils import timezone

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from schedule.models import Event
from schedule.periods import Period

from appointments.models import Appointment
from appointments.utils import send_period_reminders

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

    send_period_reminders(period)


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="task_hour_to_reminder",
    ignore_result=True
)
def task_hour_to_reminder():
    """
    tries to send a reminder approximately one hour before an appointment
    """
    fro = timezone.now()
    to = datetime(year=fro.year, month=fro.month, day=fro.day,
                  hour=fro.hour + 1, tzinfo=timezone.get_current_timezone())
    period = Period(Event.objects.exclude(appointment=None), fro, to)

    send_period_reminders(period)
