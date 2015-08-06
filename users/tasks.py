from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from users.utils import send_birthday_greetings

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute=0, hour=10)),
    name="task_birthday_greetings",
    ignore_result=True
)
def task_birthday_greetings():
    """
    Sends a greeting to all the people who have a birthday today
    """
    return send_birthday_greetings()
