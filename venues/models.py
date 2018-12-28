from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core import labels
from customers.models import Customer


class Venue(models.Model):
    """
    Model to store "schedules"
    """

    SHOW_CLIENT_NAME = '1'
    SHOW_CLIENT_PHONE = '2'
    SHOW_CLIENT_EMAIL = '3'
    SHOW_CLIENT_ID = '4'
    SHOW_CLIENT_NAME_AND_ID = '5'
    SHOW_CLIENT_NAME_PHONE_AND_ID = '6'
    SHOW_APPOINTMENT_TITLE = '7'

    CLIENT_DISPLAY_CHOICES = (
        (SHOW_CLIENT_NAME, _('Client Name')),
        (SHOW_CLIENT_PHONE, _('Client Phone')),
        (SHOW_CLIENT_EMAIL, _('Client Email')),
        (SHOW_CLIENT_ID, _('Client ID')),
        (SHOW_CLIENT_NAME_AND_ID, _('Client Name & Client ID')),
        (SHOW_CLIENT_NAME_PHONE_AND_ID,
         _('Client Name, Client Phone & Client'
           ' ID')),
        (SHOW_APPOINTMENT_TITLE, _('Appointment Title')),
    )

    NUMBER_OF_DAYS_CHOICES = [(x, "{}".format(x)) for x in range(1, 8)]

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(
        verbose_name=getattr(labels, 'VENUE', _("Schedule")),
        max_length=255,
        blank=True)
    creator = models.ForeignKey(
        User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(
        Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    main_calendar = models.BooleanField(
        _("Display in main calendar"),
        default=True,
        help_text=_(
            "Should this schedule be displayed in the main Dashboard calendar?"
        ))
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Designates whether this '
                    'schedule should be treated as'
                    ' active.'))
    shown_days = models.PositiveIntegerField(
        _("Number of days to show in calendar"),
        choices=NUMBER_OF_DAYS_CHOICES,
        default=6)
    allow_overlap = models.BooleanField(
        _("Allow appointment overlap"),
        default=False,
        help_text=_(
            "Should we allow two or more appointments at the same time?"))
    send_sms = models.BooleanField(
        _("SMS reminder"),
        default=True,
        help_text=_("Should we send reminders by text message (SMS)?"))
    send_email = models.BooleanField(
        _("Email reminder"),
        default=True,
        help_text=_("Should we send reminders by email?"))
    # reminder stuff
    custom_reminder = models.BooleanField(
        _("Use custom script"),
        default=False,
        help_text=_(
            "If you check this, we will use the custom script provided by you "
            "below.  Leave it blank to use the system default."))
    reminder_sender = models.EmailField(
        _("Reminder from address"),
        blank=False,
        default=settings.REMINDER_FROM_EMAIL_ONLY)
    reminder_subject = models.CharField(
        _("Reminder subject line"),
        max_length=100,
        blank=False,
        default=_(
            "Reminder Appointment with $OUR_NAME at $APPOINTMENT_DATE from "
            "$APPOINTMENT_START_TIME"))
    reminder_email = models.TextField(
        _("Reminder email message"),
        blank=False,
        default=_(
            "We wanted to remind you that you have an appointment at $OUR_NAME"
            " on $APPOINTMENT_DATE from $APPOINTMENT_START_TIME. Please be on"
            " time."))
    reminder_sms = models.CharField(
        _("Reminder SMS message"),
        max_length=255,
        blank=False,
        default=_(
            "Reminder! Appointment with $OUR_NAME on $APPOINTMENT_DATE from "
            "$APPOINTMENT_START_TIME"))
    show_confirm_link = models.BooleanField(
        _("Show a link to confirm appointment"), default=True, blank=False)
    show_cancel_link = models.BooleanField(
        _("Show a link to cancel appointment"), default=True, blank=False)
    # client display
    client_display = models.CharField(
        _("Client Display"),
        max_length=1,
        choices=CLIENT_DISPLAY_CHOICES,
        blank=False,
        default=SHOW_CLIENT_NAME,
        help_text=_(
            "How should the client be represented in the calendar?  This will "
            "be used only on this schedule's calendar."))

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
        return self.openinghour_set.exclude(from_hour=None).exclude(
            to_hour=None).order_by('from_hour').first()

    def closing_time(self):
        """
        returns the venue's closing time object with latest to_hour
        """
        return self.openinghour_set.exclude(from_hour=None).exclude(
            to_hour=None).order_by('to_hour').last()

    def opening_hours(self):
        return self.openinghour_set.all()

    def __str__(self):
        return self.name


class View(models.Model):
    """
    A view is a group of venues that are displayed together
    """
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    name = models.CharField(_("Name"), max_length=255, blank=False)
    venues = models.ManyToManyField(
        Venue,
        verbose_name=getattr(labels, 'VENUE_PLURAL', _("Schedules")),
        blank=False)
    customer = models.ForeignKey(
        Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = getattr(labels, 'VIEW', _("View"))
        verbose_name_plural = getattr(labels, 'VIEW_PLURAL', _("Views"))
        ordering = ['name']

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return reverse('venues:views_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('venues:views_delete', args=[self.pk])

    def get_list_url(self):
        return reverse('venues:views_list')

    def __str__(self):
        return self.name
