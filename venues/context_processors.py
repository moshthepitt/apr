from venues.models import Venue


def venue_processor(request):
    if request.user.userprofile.customer:
        result = Venue.objects.filter(customer=request.user.userprofile.customer).exclude(is_active=False)
    else:
        result = []
    return {'active_venues': result}
