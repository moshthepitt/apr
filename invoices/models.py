from django.db import models
from django.utils.translation import ugettext_lazy as _

from customers.models import Customer
from subscriptions.models import Subscription


class Invoice(models.Model):

    PAID = u'1'
    CANCELED = u'2'
    PENDING = u'3'
    FAILED = u'4'
    PARTLY_PAID = u'5'

    CASH = u'1'
    CHEQUE = u'2'
    LIPA_NA_MPESA = u'3'

    STATUS_CHOICES = (
        (PAID, _('Paid')),
        (CANCELED, _('Canceled')),
        (PENDING, _('Pending')),
        (FAILED, _('Failed')),
        (PARTLY_PAID, _('Partly Paid')),
    )

    METHOD_CHOICES = (
        (CASH, _('Cash')),
        (CHEQUE, _('Cheque')),
        (LIPA_NA_MPESA, _('Lipa na MPESA')),
    )

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))
    date = models.DateField(_("Date"))
    name = models.CharField(_("Name of payee"), max_length=255, blank=True)
    description = models.CharField(_("Description"), max_length=255)
    amount = models.DecimalField(_("Amount"), decimal_places=2, max_digits=64)
    currency = models.CharField(_("Currency"), max_length=3, default=_("KES"))
    paid_amount = models.DecimalField(
        _("Paid amount"), decimal_places=2, max_digits=64, blank=True, null=True, default=None)
    paid_currency = models.CharField(
        _("Paid currency"), max_length=3, blank=True, null=True, default=None)
    processing_fee = models.DecimalField(
        _("Processing fee"), decimal_places=2, max_digits=64, blank=True, null=True, default=None)
    status = models.CharField(
        _("Status"), max_length=1, choices=STATUS_CHOICES, blank=False, default='3',)
    method = models.CharField(
        _("Method"), max_length=1, choices=METHOD_CHOICES, blank=False)
    subscription_period_start = models.DateTimeField(
        _("Subscription Period Start"), blank=True, null=True, default=None)
    subscription_period_end = models.DateTimeField(
        _("Subscription Period End"), blank=True, null=True, default=None)
    upgrade_to = models.ForeignKey(Subscription, on_delete=models.PROTECT, blank=True, null=True, default=None, verbose_name=_(
        "Upgrade to Subscription"), help_text=_("Use this field in case the payment was for a subscription upgrade/downgrade"))

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)


class MPESAReceipt(models.Model):
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))
    receipt = models.CharField(_("MPESA Confirmation Code"), max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, verbose_name=_("Invoice"))

    class Meta:
        verbose_name = _("MPESA Receipt")
        verbose_name_plural = _("MPESA Receipts")

    def __str__(self):
        return self.receipt
