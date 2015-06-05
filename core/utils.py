from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


def invalidate_caches(name, param_list):
    key = make_template_fragment_key(name, param_list)
    cache.delete(key)
