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
    run_every=(crontab(minute=0, hour=18)),
    name="task_48hrbefore_reminders",
    ignore_result=True
)
def task_48hrbefore_reminders():
    """
    Sends a reminder to all the UN-NOTIFIED appointments
    happening in the next 48hrs
    currently sends at 6pm
    """
    t = timezone.now().date()
    fro = datetime(
        year=t.year, month=t.month, day=t.day, hour=0,
        tzinfo=timezone.get_current_timezone())
    fro = fro + timedelta(2)
    to = fro + timedelta(1)
    period = Period(Event.objects.exclude(appointment=None).exclude(
        appointment__client=None).exclude(
        appointment__status=Appointment.NOTIFIED).exclude(
        appointment__status=Appointment.CANCELED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = list(set([x.event.id for x in event_objects]))

    send_period_reminders(event_ids, sendsms=True, mailgun_campaign_id="fi0bc")


@periodic_task(
    run_every=(crontab(minute=0, hour=18)),
    name="task_day_before_reminders",
    ignore_result=True
)
def task_day_before_reminders():
    """
    Sends a reminder to all the UN-NOTIFIED appointments
    happening the next day
    currently sends at 6pm
    """
    t = timezone.now().date()
    fro = datetime(
        year=t.year, month=t.month, day=t.day, hour=0,
        tzinfo=timezone.get_current_timezone())
    fro = fro + timedelta(1)
    to = fro + timedelta(1)
    period = Period(Event.objects.exclude(appointment=None).exclude(
        appointment__client=None).exclude(
        appointment__status=Appointment.NOTIFIED).exclude(
        appointment__status=Appointment.CANCELED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = list(set([x.event.id for x in event_objects]))

    send_period_reminders(event_ids, sendsms=True, mailgun_campaign_id="fi0bc")


@periodic_task(
    run_every=(crontab(minute=0, hour=7)),
    name="task_morning_reminders",
    ignore_result=True
)
def task_morning_reminders():
    """
    Sends a reminder to all the appointments happening today
    currently sends at 7am
    """
    t = timezone.now().date()
    fro = datetime(year=t.year, month=t.month, day=t.day, hour=7,
                   tzinfo=timezone.get_current_timezone())
    to = fro + timedelta(1)
    period = Period(Event.objects.exclude(appointment=None).exclude(
        appointment__client=None).exclude(
        appointment__status=Appointment.CANCELED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = list(set([x.event.id for x in event_objects]))

    send_period_reminders(event_ids, sendsms=True, mailgun_campaign_id="ffz23")


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

    The idea is to catch any appointments happening soon that have NOT been
    notified
    """
    t = timezone.localtime(timezone.now())
    fro = t + timedelta(minutes=46)
    to = t + timedelta(hours=1)

    period = Period(Event.objects.exclude(appointment=None).exclude(
        appointment__client=None).exclude(
        appointment__status=Appointment.NOTIFIED).exclude(
        appointment__status=Appointment.CANCELED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = list(set([x.event.id for x in event_objects]))

    send_period_reminders(
        event_ids, sendsms=True, turn_off_reminders=True,
        mailgun_campaign_id="fi0bd")


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="task_immediate_reminder",
    ignore_result=True
)
def task_immediate_reminder():
    """
    tries to send a reminder for appointments happening in the next 45 minutes
    that have NOT been notified probably these were created very soon before
    the appointment start and thus were not caught by any other task

    The idea is to catch any appointments happening very soon that have NOT
    been notified
    """
    t = timezone.localtime(timezone.now())
    fro = t
    to = t + timedelta(minutes=45)

    period = Period(Event.objects.exclude(appointment=None).exclude(
        appointment__client=None).exclude(
        appointment__status=Appointment.NOTIFIED).exclude(
        appointment__status=Appointment.CANCELED), fro, to)
    event_objects = period.get_occurrences()
    event_ids = list(set([x.event.id for x in event_objects]))

    send_period_reminders(
        event_ids, sendsms=True, turn_off_reminders=True,
        mailgun_campaign_id="fi0cz")


@task(
    name="task_send_cancel_email",
    ignore_result=True
)
def task_send_cancel_email(appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        pass
    else:
        send_cancel_email(appointment)


@task(
    name="task_refresh_caches",
    ignore_result=True
)
def task_refresh_caches(appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        pass
    else:
        appointment.clear_caches()
        appointment.set_caches()
