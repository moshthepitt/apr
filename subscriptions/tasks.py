# from django.utils import timezone

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute=0, hour=9)),
    name="task_notify_renewal_near",
    ignore_result=True
)
def task_notify_renewal_near():
    """
    attempt to send a notice to customers whose subscription
    is about to end in 3 days or less
    notify customer so that they may pay
    """
    # t = timezone.localtime(timezone.now())
    pass


@periodic_task(
    run_every=(crontab(minute=0, hour=9)),
    name="task_notify_subscription_end",
    ignore_result=True
)
def task_notify_subscription_end():
    """
    attempt to find subscriptions that should have ended yesterday
    makes these subscriptions inactive
    and notify customer
    """
    # t = timezone.localtime(timezone.now())
    pass
