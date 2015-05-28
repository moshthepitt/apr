from django.utils.translation import ugettext as _
from venues.models import Venue


def new_default_venue(customer):
    venue = Venue(
        name=_("default"),
        creator=customer.user,
        customer=customer
    )
    venue.save()
    return venue
