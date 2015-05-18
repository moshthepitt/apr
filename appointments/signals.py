from django.db.models.signals import post_delete
from django.dispatch import receiver

from appointments.models import Appointment


@receiver(post_delete, sender=Appointment)
def event_delete(sender, instance, **kwargs):
    """
    When an appointment is deleted, we proceed to delete the Event Object that it references
    """
    if instance.event:
        this_event = instance.event
        this_event.delete()
