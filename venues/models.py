from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from core import labels

from customers.models import Customer


class Venue(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_('Venue name'), max_length=255, blank=True)
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    main_calendar = models.BooleanField(_("Display in main calendar"), default=True, help_text=_(
        "Should this schedule be displayed in the main Dashboard calendar?"))
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this schedule should be treated as '
                                                'active.'))
    # reminder stuff
    custom_reminder = models.BooleanField(_("Use custom script"), default=False, help_text=_(
        "If you check this, we will use the custom script provided by you below.  Leave it blank to use the system default."))
    reminder_sender = models.EmailField(
        _("Reminder from address"), blank=False, default=settings.REMINDER_FROM_EMAIL_ONLY)
    reminder_subject = models.CharField(_("Reminder subject line"), max_length=100, blank=False, default=_(
        "Reminder Appointment with $OUR_NAME at $APPOINTMENT_DATE from $APPOINTMENT_START_TIME"))
    reminder_email = models.TextField(_("Reminder email message"), blank=False, default=_(
        "We wanted to remind you that you have an appointment at $OUR_NAME on $APPOINTMENT_DATE from $APPOINTMENT_START_TIME. Please be on time."))
    reminder_sms = models.CharField(_("Reminder SMS message"), max_length=255, blank=False, default=_(
        "Reminder! Appointment with $OUR_NAME on $APPOINTMENT_DATE from $APPOINTMENT_START_TIME"))
    show_confirm_link = models.BooleanField(
        _("Show a link to confirm appointment"), default=True, blank=False)
    show_cancel_link = models.BooleanField(
        _("Show a link to cancel appointment"), default=True, blank=False)

    class Meta:
        verbose_name = getattr(labels, 'VENUE', _("Schedule"))
        verbose_name_plural = getattr(labels, 'VENUE_PLURAL', _("Schedules"))
        ordering = ['name']

    def meta(self):
        return self._meta

    def get_absolute_url(self):
        return reverse('venues:venue', args=[self.pk])

    def opening_time(self):
        """
        returns the venue's opening time object with earliest from_hour
        """
        return self.openinghour_set.exclude(from_hour=None).exclude(to_hour=None).order_by('from_hour').first()

    def closing_time(self):
        """
        returns the venue's closing time object with latest to_hour
        """
        return self.openinghour_set.exclude(from_hour=None).exclude(to_hour=None).order_by('to_hour').last()

    def opening_hours(self):
        return self.openinghour_set.all()

    def __str__(self):
        return self.name


# ### S I G N A L S ####
from venues import signals
