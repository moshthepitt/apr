"""
Apps module for core app
"""
from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        """Run when ready"""
        from users import signals  # noqa
        from venues import signals  # noqa
