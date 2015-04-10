from django.views.generic.detail import DetailView

from venues.models import Venue


class VenueView(DetailView):
    model = Venue
    template_name = "venues/venue_calendar.html"
