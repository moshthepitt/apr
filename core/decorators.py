import hashlib

from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs


def apr_cache(timeout):
    """
    creates a cache_page that takes into account the current customer
    and the full request, including GET parameters
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            customer_key = request.user.userprofile.customer.pk
            request_key = hashlib.md5(request.build_absolute_uri()).hexdigest()
            return cache_page(timeout, key_prefix="_apr_cache_{0}_{1}".format(
                customer_key, request_key)
            )(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator
