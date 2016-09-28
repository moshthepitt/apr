from datetime import timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from customers.utils import customer_has_subscription


class Customer(models.Model):

    """
    This model stores customers i.e. people who sign up to user APR
    """
    DAY = 1
    WEEK = 2
    MONTH = 3
    YEAR = 4

    TIME_UNIT_CHOICES = [
        (DAY, _("Day")),
        (WEEK, _("Week")),
        (MONTH, _("Month")),
        (YEAR, _("Year")),
    ]

    WEEKDAYS = 7
    MONTHDAYS = 30.44
    YEARDAYS = 365.25

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
        (SHOW_CLIENT_NAME_PHONE_AND_ID, _('Client Name, Client Phone & Client ID')),
        (SHOW_APPOINTMENT_TITLE, _('Appointment Title')),
    )

    NUMBER_OF_DAYS_CHOICES = [(x, "{}".format(x)) for x in range(1, 8)]

    user = models.ForeignKey(User, verbose_name=_("User"), null=True, default=None, blank=True,
                             on_delete=models.PROTECT, help_text=_("This user will be able to log in as this customer"))
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    name = models.CharField(_('Customer name'), max_length=255, blank=False)
    email = models.EmailField(_('Email address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this customer should be treated as '
                                                'active.'))
    shown_days = models.PositiveIntegerField(
        _("Number of days to show in main calendar"), choices=NUMBER_OF_DAYS_CHOICES, default=6)
    allow_overlap = models.BooleanField(_("Allow appointment overlap"), default=False, help_text=_(
        "Should we allow two or more appointments at the same time?"))
    send_sms = models.BooleanField(
        _("SMS reminder"), default=True, help_text=_("Should we send reminders by text message (SMS)?"))
    send_email = models.BooleanField(
        _("Email reminder"), default=True, help_text=_("Should we send reminders by email?"))
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
    # client display
    client_display = models.CharField(_("Client Display"), max_length=1, choices=CLIENT_DISPLAY_CHOICES, blank=False, default=SHOW_CLIENT_NAME, help_text=_(
        "How should the client be represented in the calendar?"))
    # greetings
    birthday_greeting_active = models.BooleanField(_("Activate birthday greetings"), help_text=_(
        "Birthday greetings are sent to clients on their birth days"), default=False)
    birthday_greeting_sender = models.EmailField(
        _("Birthday greeting from address"), blank=False, default=settings.REMINDER_FROM_EMAIL_ONLY)
    birthday_greeting_subject = models.CharField(_("Birthday greeting subject line"), max_length=100, blank=False, default=_(
        "Happy Birthday, $FIRST_NAME"))
    birthday_greeting_email = models.TextField(_("Birthday greeting email message"), blank=False, default=_(
        "We are thinking of you on this important day and hope that it is filled with happiness. Wishing you many joyous years ahead!"))
    birthday_greeting_sms = models.CharField(_("Birthday greeting SMS message"), max_length=255, blank=False, default=_(
        "Happy Birthday! Wishing you all the best today and always! $OUR_NAME"))
    birthday_greeting_send_email = models.BooleanField(
        _("Birthday greeting send email"), default=True)
    birthday_greeting_send_sms = models.BooleanField(_("Birthday greeting send SMS"), default=True)
    # Rebooking
    rebooking_active = models.BooleanField(
        _("Activate Rebooking"), help_text=_(
            "These are booking reminders which are sent to clients a while after their last appointment to encourage them to book a new appointment"), default=False)
    rebooking_period = models.PositiveIntegerField(
        _("Rebooking period length"), blank=True, default=6)
    rebooking_period_unit = models.PositiveIntegerField(
        _("Rebooking period units"), choices=TIME_UNIT_CHOICES, default=MONTH)
    rebooking_sender = models.EmailField(
        _("Rebooking from address"), blank=False, default=settings.REMINDER_FROM_EMAIL_ONLY)
    rebooking_subject = models.CharField(_("Rebooking subject line"), max_length=100, blank=False, default=_(
        "$FIRST_NAME, we miss you"))
    rebooking_email = models.TextField(_("Rebooking email message"), blank=False, default=_(
        "We wanted to remind you that your next appointment is due soon.  Feel free to call us on $OUR_PHONE to book an appointment."))
    rebooking_sms = models.CharField(_("Rebooking SMS message"), max_length=255, blank=False, default=_(
        "Your next appointment with $OUR_NAME is due soon. Call $OUR_PHONE to book."))
    rebooking_send_email = models.BooleanField(_("Rebooking send email"), default=True)
    rebooking_send_sms = models.BooleanField(_("Rebooking send SMS"), default=True)
    use_tags = models.BooleanField(_("Use Tags"), default=False, help_text=_("Tags are used to classify appointments"))
    use_four_day = models.BooleanField(_("Activate Three-day View"), default=False)
    use_no_background_print = models.BooleanField(_("No background color on print"), default=False)
    time_slot_height = models.IntegerField(_("Time Slot Height"), default=25, help_text=_('The height of each timeslot in pixels. Calendar event text is scaled relative to the timeslot height.'))
    time_slots_per_hour = models.IntegerField(_("Time Slots Per Hour"), default=4, help_text=_("The number of timeslots that will be available within an hour."))

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def meta(self):
        return self._meta

    def global_opening_time(self):
        """
        returns the customer's opening time object with earliest from_hour
        """
        return self.openinghour_set.exclude(from_hour=None).exclude(to_hour=None).exclude(venue__main_calendar=False).order_by('from_hour').first()

    def global_closing_time(self):
        """
        returns the customer's closing time object with latest to_hour
        """
        return self.openinghour_set.exclude(from_hour=None).exclude(to_hour=None).exclude(venue__main_calendar=False).order_by('to_hour').last()

    def has_subscription(self):
        return customer_has_subscription(self)

    def number_of_venues(self):
        return self.venue_set.all().count()

    def is_new(self):
        return (timezone.now() - self.created_on) < timedelta(days=3)
