from venues.models import Venue, View


def venue_processor(request):
    views = View.objects.filter(customer=request.user.userprofile.customer)
    if request.user.is_authenticated():
        result = Venue.objects.filter(
            customer=request.user.userprofile.customer).exclude(
            is_active=False)
    else:
        result = []
    return {'active_venues': result, 'active_views': views}
