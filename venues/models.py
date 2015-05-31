from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from core import labels

from customers.models import Customer


class Venue(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_('Venue name'), max_length=255, blank=True)
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this venue should be treated as '
                                                'active.'))

    class Meta:
        verbose_name = getattr(labels, 'VENUE', _("Venue"))
        verbose_name_plural = getattr(labels, 'VENUE_PLURAL', _("Venues"))
        ordering = ['name']

    def meta(self):
        return self._meta

    def get_absolute_url(self):
        return reverse('venues:venue', args=[self.pk])

    def __str__(self):
        return self.name
