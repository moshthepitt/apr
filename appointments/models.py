from schedule.models import Event

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import Client

class Appointment(models.Model):
    """
    A way to associate users with events
    """
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    creator = models.ForeignKey(User, verbose_name=_("Creator"),  on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name=_("Client"), on_delete=models.PROTECT)
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.PROTECT)

    def __unicode__(self):
        return _("Appointment: %s - %s") % (self.client,self.event)
