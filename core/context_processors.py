from django.contrib.sites.models import Site
from django.conf import settings


def debug_processor(request):
    """Makes DEBUG_MODE available if settings.DEBUG is True"""
    return {'DEBUG_MODE': settings.DEBUG}


def site_processor(request):
    return {'site': Site.objects.get_current()}
