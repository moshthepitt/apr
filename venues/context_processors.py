from venues.models import Venue


def venue_processor(request):
    return {'active_venues': Venue.objects.exclude(appointment=None)}
