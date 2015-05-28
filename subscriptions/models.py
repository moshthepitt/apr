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

    name = models.CharField(_("Name"), max_length=100, unique=True, null=False)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=64, decimal_places=2)
    trial_period = models.PositiveIntegerField(_("Trial Period Length"), blank=True, default=15)
    trial_unit = models.CharField(
        _("Trial Period Units"), max_length=1, choices=TIME_UNIT_CHOICES, default=DAY)
    recurring_period = models.PositiveIntegerField(
        _("Recurring Period Length"), blank=True, default=1)
    recurring_unit = models.CharField(
        _("Recurring Period Units"), max_length=1, choices=TIME_UNIT_CHOICES, default=MONTH)
    highlighted = models.BooleanField(_("Highlighted"), default=True, help_text=_(
        "Is this subscription highlighted for prominent display?"))

    class Meta:
        ordering = ('price', '-recurring_period')
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

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

    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), null=False, blank=False)
    subscription = models.ForeignKey(
        Subscription, verbose_name=_("Subscription"), null=False, blank=False)
    start = models.DateTimeField(default=timezone.now, verbose_name=_("Subscription Date"))
    current_period_start = models.DateTimeField(null=True, verbose_name=_("Period Start"))
    current_period_end = models.DateTimeField(null=True, verbose_name=_("Period End"))
    ended_at = models.DateTimeField(_("Ended at"), null=True, blank=True)
    trial_end = models.DateTimeField(_("Trial end"), null=True, blank=True)
    trial_start = models.DateTimeField(_("Trial start"), null=True, blank=True)
    cancel_at_period_end = models.BooleanField(_("Cancel at period end"), default=False)
    canceled_at = models.DateTimeField(_("Canceled at"), null=True, blank=True)
    cancel_reason = models.TextField(
        blank=True, null=True, default=None, verbose_name=_("Reason for cancelling"))
    status = models.CharField(_("Status"), max_length=1, null=True, choices=STATUS_CHOICES, default=TRIALING)

    class Meta:
        unique_together = (('customer', 'subscription'), )
        verbose_name = _("Customer Subscription")
        verbose_name_plural = _("Customer Subscriptions")

    def __str__(self):
        return "{customer} {sub}".format(user=self.customer, sub=self.subscription)
