from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

from customers.utils import customer_has_subscription


class Customer(models.Model):

    """
    This model stores customers i.e. peopl who sign up to user APR
    """
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, default=None, blank=True,
                             on_delete=models.PROTECT, help_text=_("This user will be able to log in as this customer"))
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    name = models.CharField(_('Customer name'), max_length=255, blank=False)
    email = models.EmailField(_('Email address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this assistant should be treated as '
                                                'active.'))

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
        return self.openinghour_set.exclude(break_time=True).order_by('from_hour').first()

    def global_closing_time(self):
        """
        returns the customer's closing time object with latest to_hour
        """
        return self.openinghour_set.exclude(break_time=True).order_by('to_hour').last()

    def has_subscription(self):
        return customer_has_subscription(self)

    def number_of_venues(self):
        return self.venue_set.all().count()
