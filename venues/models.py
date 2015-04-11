from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from core import labels


class Venue(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_('Venue name'), max_length=255, blank=True)
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = getattr(labels, 'VENUE', _("Venue"))
        verbose_name_plural = getattr(labels, 'VENUE_PLURAL', _("Venues"))
        ordering = ['name']

    def meta(self):
        return self._meta

    def __str__(self):
        return self.name
