from django.db import models
from django.utils.translation import ugettext_lazy as _

from customers.models import Customer
from appointments.models import Appointment


class Reminder(models.Model):
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    appointment = models.ForeignKey(
        Appointment, verbose_name=_("Appointment"), on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    client_name = models.CharField(_("Client Name"), max_length=255)
    appointment_time = models.DateTimeField(_("Appointment Time"))
    sent_email = models.BooleanField(_("Sent email"), default=False)
    sent_sms = models.BooleanField(_("Sent sms"), default=False)

    @property
    def _appointment_id(self):
        if self.appointment:
            return self.appointment.id
        return None

    class Meta:
        verbose_name = _("Reminder")
        verbose_name_plural = _("Reminders")

    def __str__(self):
        return self.client_name
