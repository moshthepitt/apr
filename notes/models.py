from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from venues.models import Venue
from customers.models import Customer

from core import labels


class Note(models.Model):
    TOP = '1'
    BOTTOM = '2'

    TYPE_CHOICES = (
        (TOP, _('Top')),
        (BOTTOM, _('Bottom')),
    )

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    date = models.DateField(_("Date"))
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    venue = models.ForeignKey(Venue, verbose_name=getattr(
        labels, 'VENUE', _("Venue")), blank=True, null=True, default=None, on_delete=models.PROTECT)
    note = models.TextField(_("Note"), blank=False)
    note_type = models.CharField(_("Type"), max_length=1, choices=TYPE_CHOICES, blank=False, default=TOP)
    featured = models.BooleanField(_("Featured"), default=False)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        ordering = ['-date', 'id']

    def __str__(self):
        return self.note
