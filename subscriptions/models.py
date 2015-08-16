from datetime import timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from customers.models import Customer


class Subscription(models.Model):
    NONE = 0
    DAY = 1
    WEEK = 2
    MONTH = 3
    YEAR = 4

    TIME_UNIT_CHOICES = [
        (NONE, _("None")),
        (DAY, _("Day")),
        (WEEK, _("Week")),
        (MONTH, _("Month")),
        (YEAR, _("Year")),
    ]

    WEEKDAYS = 7
    MONTHDAYS = 30.44
    YEARDAYS = 365.25

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_("Name"), max_length=100, unique=True, null=False)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=64, decimal_places=2)
    trial_period = models.PositiveIntegerField(_("Trial Period Length"), blank=True, default=15)
    trial_unit = models.PositiveIntegerField(
        _("Trial Period Units"), choices=TIME_UNIT_CHOICES, default=DAY)
    recurring_period = models.PositiveIntegerField(
        _("Recurring Period Length"), blank=True, default=1)
    recurring_unit = models.PositiveIntegerField(
        _("Recurring Period Units"), choices=TIME_UNIT_CHOICES, default=MONTH)
    max_appointments = models.PositiveIntegerField(_("Max Appointments"), blank=False, default=500)
    max_schedules = models.PositiveIntegerField(_("Max Schedules"), blank=False, default=10)
    highlighted = models.BooleanField(_("Highlighted"), default=True, help_text=_(
        "Is this subscription highlighted for prominent display?"))
    default = models.BooleanField(_("Default"), default=False, help_text=_(
        "The default subscription will be highlighted in price tables.  Ideally only one subscription should be default."))
    hidden = models.BooleanField(_("Hidden"), default=False)
    can_print = models.BooleanField(_("Can Print"), default=False)

    class Meta:
        ordering = ('price', '-recurring_period')
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def get_subscription_days(self):
        """
        returns the number of days as subscription Length
        """
        if self.recurring_unit == self.DAY:
            return self.recurring_period
        elif self.recurring_unit == self.WEEK:
            return self.recurring_period * self.WEEKDAYS
        elif self.recurring_unit == self.MONTH:
            return self.recurring_period * self.MONTHDAYS
        elif self.recurring_unit == self.YEAR:
            return self.recurring_period * self.YEARDAYS
        else:
            return 0

    def get_trialing_days(self):
        """
        returns the number of days as trial Length
        """
        if self.trial_unit == self.DAY:
            return self.trial_period
        elif self.trial_unit == self.WEEK:
            return self.trial_period * self.WEEKDAYS
        elif self.trial_unit == self.MONTH:
            return self.trial_period * self.MONTHDAYS
        elif self.trial_unit == self.YEAR:
            return self.trial_period * self.YEARDAYS
        else:
            return 0

    def __str__(self):
        return self.name


class CustomerSubscription(models.Model):
    TRIALING = 1
    ACTIVE = 2
    PAST_DUE = 3
    CANCELED = 4
    UNPAID = 5
    ENDED = 6

    STATUS_CHOICES = [
        (TRIALING, _("Trialing")),
        (ACTIVE, _("Active")),
        (PAST_DUE, _("Past Due")),
        (CANCELED, _("Canceled")),
        (UNPAID, _("Unpaid")),
        (ENDED, _("Ended")),
    ]

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    customer = models.OneToOneField(Customer, verbose_name=_("Customer"), null=False, blank=False)
    subscription = models.ForeignKey(
        Subscription, verbose_name=_("Subscription"), null=False, blank=False)
    start = models.DateTimeField(default=timezone.now, verbose_name=_("Subscription Date"))
    current_period_start = models.DateTimeField(null=True, default=None, blank=True, verbose_name=_("Period Start"))
    current_period_end = models.DateTimeField(null=True, default=None, blank=True, verbose_name=_("Period End"))
    ended_at = models.DateTimeField(_("Ended at"), null=True, blank=True)
    trial_end = models.DateTimeField(_("Trial end"), null=True, blank=True)
    trial_start = models.DateTimeField(_("Trial start"), null=True, blank=True)
    cancel_at_period_end = models.BooleanField(_("Cancel at period end"), default=False)
    canceled_at = models.DateTimeField(_("Canceled at"), null=True, blank=True)
    cancel_reason = models.TextField(
        blank=True, null=True, default=None, verbose_name=_("Reason for cancelling"))
    status = models.PositiveIntegerField(
        _("Status"), null=False, choices=STATUS_CHOICES, default=TRIALING)

    class Meta:
        unique_together = (('customer', 'subscription'), )
        verbose_name = _("Customer Subscription")
        verbose_name_plural = _("Customer Subscriptions")

    @property
    def active(self):
        return self.status == self.ACTIVE or self.status == self.TRIALING

    def start_trial(self, start_date):
        self.trial_start = start_date
        self.trial_end = start_date + timedelta(self.subscription.get_trialing_days())
        self.status = self.TRIALING
        self.save()

    def start_subscription(self, start_date):
        self.current_period_start = start_date
        self.current_period_end = start_date + timedelta(self.subscription.get_trialing_days())
        self.status = self.ACTIVE
        self.save()

    @property
    def next_charge_date(self):
        if self.status == self.TRIALING:
            return self.trial_end - timedelta(days=1)
        if self.current_period_end:
            return self.current_period_end - timedelta(days=1)
        return timezone.now()

    def __str__(self):
        return "{customer} {sub}".format(customer=self.customer, sub=self.subscription)
