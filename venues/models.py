from django.db import models
from django.utils.translation import ugettext_lazy as _

from core import labels


class Venue(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_('Venue name'), max_length=255, blank=True)

    class Meta:
        verbose_name = getattr(labels, 'VENUE', _("Venue"))
        verbose_name_plural = getattr(labels, 'VENUE_PLURAL', _("Venues"))

    def __str__(self):
        return self.name
