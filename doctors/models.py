from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

from customers.models import Customer

from core import labels


class Doctor(models.Model):

    """
    This model stores the "doctors" in the sense that clients make appointments to see doctors, typically
    """
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, default=None, blank=True,
                             on_delete=models.PROTECT, help_text=_("This user will be able to log in as this doctor"))
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    first_name = models.CharField(_('First name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True)
    email = models.EmailField(_('Email address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    creator = models.ForeignKey(User, verbose_name=_(
        "Creator"), on_delete=models.PROTECT, related_name="doctor_creator")
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this doctor should be treated as '
                                                'active.'))

    class Meta:
        verbose_name = getattr(labels, 'DOCTOR', _("Doctor"))
        verbose_name_plural = getattr(labels, 'DOCTOR_PLURAL', _("Doctors"))
        ordering = ['first_name']

    def __unicode__(self):
        return self.get_full_name()

    def meta(self):
        return self._meta

    def get_full_name(self):
        """
        Returns the title prefix, first_name plus the last_name, with a space in between.
        """
        full_name = '{} {} {}'.format(
            labels.DOCTOR_TITLE, self.first_name, self.last_name)
        return full_name.strip()
