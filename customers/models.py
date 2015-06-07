from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from customers.utils import customer_has_subscription


class Customer(models.Model):

    """
    This model stores customers i.e. peopl who sign up to user APR
    """
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, default=None, blank=True,
                             on_delete=models.PROTECT, help_text=_("This user will be able to log in as this customer"))
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    name = models.CharField(_('Customer name'), max_length=255, blank=False)
    email = models.EmailField(_('Email address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this assistant should be treated as '
                                                'active.'))
    # reminder stuff
    custom_reminder = models.BooleanField(_("Use custom reminder"), default=False, help_text=_("If you check this, we will use the custom script provided by you"))
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
        return self.openinghour_set.exclude(from_hour=None).exclude(to_hour=None).order_by('from_hour').first()

    def global_closing_time(self):
        """
        returns the customer's closing time object with latest to_hour
        """
        return self.openinghour_set.exclude(from_hour=None).exclude(to_hour=None).order_by('to_hour').last()

    def has_subscription(self):
        return customer_has_subscription(self)

    def number_of_venues(self):
        return self.venue_set.all().count()
