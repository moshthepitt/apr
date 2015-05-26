from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core import labels

from doctors.models import Doctor
from customers.models import Customer


class Client(models.Model):

    """
    This models stores clients in the sense that it is clients who come to any appointments
    """
    SELF_PAYING = '1'
    COMPANY_PAYING = '2'
    INSURANCE_PAYING = '3'
    PAYMENT_CHOICES = (
        (SELF_PAYING, _('Self')),
        (COMPANY_PAYING, _('Company')),
        (INSURANCE_PAYING, _('Insurance')),
    )

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    client_id = models.CharField(
        getattr(labels, 'CLIENT_ID', _("Client ID")), max_length=255, blank=True)
    first_name = models.CharField(_('First name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True)
    email = models.EmailField(_('Email address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    payment = models.CharField(_("Payment Method"), max_length=1, choices=PAYMENT_CHOICES, blank=False, help_text=_(
        "How will payment be made?"))
    insurance_company = models.CharField(_('Insurance Company'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this client should be treated as '
                                                'active.'))
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the client."
        return self.first_name

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return "{}".format(self.email)

    def meta(self):
        return self._meta

    class Meta:
        verbose_name = getattr(labels, 'CLIENT', _("Client"))
        verbose_name_plural = getattr(labels, 'CLIENT_PLURAL', _("Clients"))
        ordering = ['client_id']


class UserProfile(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    user = models.OneToOneField(User, verbose_name=_("User"))
    customer = models.ForeignKey(Customer, verbose_name=_(
        "Customer"), on_delete=models.PROTECT, blank=True, null=True, default=None)

    def is_doctor(self):
        "Checks if this userprofile is connected to a Doctor object"
        return self.user.doctor_set.exists()

    def is_customer(self):
        "Checks if this userprofile is the 'owner' of a Customer object"
        return self.user.customer_set.exists()

    def make_doctor(self, creator):
        """
            Creates a Doctor object attached to this userprofile
            Inputs:
                creator = a User object that represents the person who will
                be marked as having 'created' the Doctor object
        """
        if not Doctor.objects.filter(user=self.user).exists():
            doctor = Doctor(user=self.user, creator=creator)
            doctor.first_name = self.user.first_name
            doctor.last_name = self.user.last_name
            doctor.email = self.user.email
            doctor.save()

    def __str__(self):
        return _("%s's profile") % self.user


# ### S I G N A L S ####
from users import signals
