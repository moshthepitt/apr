from django.db.models.signals import post_save
from django.dispatch import receiver

from opening_hours.utils import new_default_venue_opening_hours
from venues.models import Venue


@receiver(post_save, sender=Venue)
def create_venue(sender, instance, created, **kwargs):
    if created:
        # create new venue
        new_default_venue_opening_hours(instance)
