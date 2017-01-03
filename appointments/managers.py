from django.db import models


class AppointmentManager(models.Manager):

    def get_queryset(self):
        return super(AppointmentManager, self).get_queryset().select_related(
            'customer',
            'client',
            'doctor',
            'venue',
            # 'event',
            'tag'
        )
