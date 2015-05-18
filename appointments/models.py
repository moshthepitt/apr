from schedule.models import Event

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from users.models import Client
from doctors.models import Doctor
from venues.models import Venue

from core import labels


class Appointment(models.Model):

    """
    An appointment is an Event which has a Client and optionally a Doctor & Venue
    """
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    client = models.ForeignKey(
        Client, verbose_name=getattr(labels, 'CLIENT', _("Client")), on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, verbose_name=getattr(
        labels, 'DOCTOR', _("Doctor")), blank=True, null=True, default=None, on_delete=models.PROTECT)
    venue = models.ForeignKey(Venue, verbose_name=getattr(
        labels, 'VENUE', _("Venue")), blank=True, null=True, default=None, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.PROTECT)

    def __unicode__(self):
        return _("Appointment: %s - %s - %s") % (self.client, self.doctor, self.event)

    def meta(self):
        return self._meta

    def get_absolute_url(self):
        return reverse('appointments:appointment', args=[self.pk])

    def get_form_data(self):
        """
        returns a dictionary that can be used to populate initial data from appointments.AppointmentForm
        """
        return dict(
            client=self.client.id,
            title=self.event.title,
            start_date=self.event.start.strftime('%d-%m-%Y'),
            start_time=self.event.start.strftime('%-H:%M%p'),
            end_date=self.event.end.strftime('%d-%m-%Y'),
            end_time=self.event.end.strftime('%-H:%M%p'),
            doctor=self.doctor.id,
            venue=self.venue.id,
            description=self.event.description,
        )

    class Meta:
        ordering = ['-event__start']


# ### S I G N A L S ####
from appointments import signals
