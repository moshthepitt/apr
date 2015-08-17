from schedule.models import Event

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.timezone import localtime
from django.utils.text import slugify

from randomslugfield import RandomSlugField

from users.models import Client
from doctors.models import Doctor
from venues.models import Venue
from customers.models import Customer

from core import labels


class Tag(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_("Name"), max_length=255)
    color = models.CharField(_("Color"), max_length=50, blank=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT, null=True)

    @property
    def html_name(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __unicode__(self):
        return self.name


class Appointment(models.Model):

    """
    An appointment is an Event which has a Client and optionally a Doctor & Venue
    """
    SCHEDULED = 'scheduled'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    NOTIFIED = 'notified'
    NOSHOW = 'noshow'
    SHOWED = 'showed'

    STATUS_LIST = [SCHEDULED, CONFIRMED, CANCELED, NOTIFIED, NOSHOW, SHOWED]

    STATUS_CHOICES = (
        (SCHEDULED, _('Scheduled')),
        (CONFIRMED, _('Confirmed')),
        (CANCELED, _('Canceled')),
        (NOTIFIED, _('Notified')),
        (NOSHOW, _('No Show')),
        (SHOWED, _('Showed Up')),
    )

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    slug = RandomSlugField(length=9)
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    client = models.ForeignKey(
        Client, verbose_name=getattr(labels, 'CLIENT', _("Client")), on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, verbose_name=getattr(
        labels, 'DOCTOR', _("Doctor")), blank=True, null=True, default=None, on_delete=models.PROTECT)
    venue = models.ForeignKey(Venue, verbose_name=getattr(
        labels, 'VENUE', _("Venue")), blank=True, null=True, default=None, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.PROTECT)
    status = models.CharField(_("Status"), max_length=15, choices=STATUS_CHOICES, blank=False, default=SCHEDULED)
    no_reminders = models.BooleanField(_("No Reminders"), default=False, help_text=_("Do not send reminders for this appointment"))
    tag = models.ForeignKey(Tag, verbose_name=_("Tag"), null=True, default=None, blank=True)

    def __unicode__(self):
        return _("{client} - {venue} - {event}").format(client=self.client, venue=self.venue, event=self.event)

    def meta(self):
        return self._meta

    def get_absolute_url(self):
        return reverse('appointments:appointment', args=[self.pk])

    def get_doctor_id(self):
        if self.doctor:
            return self.doctor.id
        return None

    def get_form_data(self):
        """
        returns a dictionary that can be used to populate initial data from appointments.AppointmentForm
        """
        return dict(
            client=self.client.id,
            title=self.event.title,
            start_date=localtime(self.event.start).strftime('%d-%m-%Y'),
            start_time=localtime(self.event.start).strftime('%-H:%M%p'),
            end_date=localtime(self.event.end).strftime('%d-%m-%Y'),
            end_time=localtime(self.event.end).strftime('%-H:%M%p'),
            doctor=self.get_doctor_id(),
            venue=self.venue.id,
            description=self.event.description,
        )

    class Meta:
        ordering = ['-event__start']


# ### S I G N A L S ####
from appointments import signals
