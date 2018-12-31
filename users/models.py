from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core import labels
from customers.models import Customer
from doctors.models import Doctor
from phonenumber_field.modelfields import PhoneNumberField

from venues.models import Venue


class Client(models.Model):
    """
    This models stores clients in the sense that it is clients who come to any
    appointments
    """
    SELF_PAYING = '1'
    COMPANY_PAYING = '2'
    INSURANCE_PAYING = '3'
    PAYMENT_CHOICES = (
        (SELF_PAYING, _('Self')),
        (COMPANY_PAYING, _('Company')),
        (INSURANCE_PAYING, _('Insurance')),
    )

    ADULT = 'Adult'
    DEPENDANT = 'Dependant'
    ADULT_DEPENDANT_CHOICES = (
        (ADULT, _(ADULT)),
        (DEPENDANT, _(DEPENDANT)),
    )

    NEW = '1'
    UNKNOWN = '2'
    COMPLETE = '3'
    STATUS_CHOICES = (
        (NEW, _("New")),
        (UNKNOWN, _("Unknown")),
        (COMPLETE, _("Complete")),
    )
    ADD_STATUS_CHOICES = (
        (NEW, _("New")),
        (UNKNOWN, _("Unknown")),
    )
    COMPLETE_STATUS_CHOICES = (
        (COMPLETE, _("Complete")),
    )

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    client_id = models.CharField(
        getattr(labels, 'CLIENT_ID', _("Client ID")),
        max_length=255,
        blank=True,
        unique=False,
        help_text=_(
            "Optional unique client ID.  Will be auto-generated if left blank"
        ))
    first_name = models.CharField(_('First name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True)
    birth_date = models.DateField(
        _("Date of Birth"),
        blank=True,
        default=None,
        null=True,
        help_text=_("Needed to send birthday greetings"))
    email = models.EmailField(
        _('Email address'),
        blank=True,
        help_text=_("Needed to send reminders by email"))
    phone = PhoneNumberField(
        _('Phone Number'),
        max_length=255,
        blank=True,
        help_text=_("Needed to send reminders by SMS"))
    payment = models.CharField(
        _("Payment Method"),
        max_length=1,
        choices=PAYMENT_CHOICES,
        blank=False,
        help_text=_("How will payment be made?"))
    status = models.CharField(
        _("Status"),
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        default=COMPLETE)
    insurance_company = models.CharField(
        _('Insurance Company'), max_length=255, blank=True)
    data = JSONField(_("Data"), default=dict)
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Designates whether this client should be treated as '
                    'active.'))
    creator = models.ForeignKey(
        User, verbose_name=_("Creator"), on_delete=models.PROTECT)
    customer = models.ForeignKey(
        Customer, verbose_name=_("Customer"), on_delete=models.PROTECT)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the client."
        return self.first_name

    def get_absolute_url(self):
        return reverse('users:client', args=[self.pk])

    def display_name(self, venue=None, title=None):
        if venue:
            if venue.client_display == Venue.SHOW_CLIENT_PHONE:
                return "{}".format(self.phone)
            elif venue.client_display == Venue.SHOW_CLIENT_EMAIL:
                return "{}".format(self.email)
            elif venue.client_display == Venue.SHOW_CLIENT_ID:
                return "{}".format(self.client_id)
            elif venue.client_display == Venue.SHOW_CLIENT_NAME_AND_ID:
                return "{name} {client_id}".format(
                    name=self.__str__(), client_id=self.client_id)
            elif venue.client_display == Venue.SHOW_CLIENT_NAME_PHONE_AND_ID:
                if self.phone:
                    return "{name} {phone} {client_id}".format(
                        name=self.__str__(),
                        phone=self.phone,
                        client_id=self.client_id)
                else:
                    return "{name} {client_id}".format(
                        name=self.__str__(), client_id=self.client_id)
            elif venue.client_display == Venue.SHOW_APPOINTMENT_TITLE and\
                    title:
                return "{}".format(title)
        elif self.customer.client_display != Customer.SHOW_CLIENT_NAME:
            if self.customer.client_display == Customer.SHOW_CLIENT_PHONE:
                return "{}".format(self.phone)
            elif self.customer.client_display == Customer.SHOW_CLIENT_EMAIL:
                return "{}".format(self.email)
            elif self.customer.client_display == Customer.SHOW_CLIENT_ID:
                return "{}".format(self.client_id)
            elif self.customer.client_display ==\
                    Customer.SHOW_CLIENT_NAME_AND_ID:
                return "{name} {client_id}".format(
                    name=self.__str__(), client_id=self.client_id)
            elif self.customer.client_display ==\
                    Customer.SHOW_CLIENT_NAME_PHONE_AND_ID:
                if self.phone:
                    return "{name} {phone} {client_id}".format(
                        name=self.__str__(),
                        phone=self.phone,
                        client_id=self.client_id)
                else:
                    return "{name} {client_id}".format(
                        name=self.__str__(), client_id=self.client_id)
            elif self.customer.client_display ==\
                    Customer.SHOW_APPOINTMENT_TITLE and title:
                return "{}".format(title)

        return self.get_full_name()

    def get_last_appointment(self):
        return self.appointment_set.order_by('-event__start').first()

    @property
    def last_appointment(self):
        return self.get_last_appointment()

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
    ADMIN = '1'
    EDITOR = '2'
    USER = '3'
    ROLE_CHOICES = (
        (ADMIN, _('Admin')),
        (EDITOR, _('Editor')),
        (USER, _('User')),
    )

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    user = models.OneToOneField(User, verbose_name=_("User"))
    customer = models.ForeignKey(
        Customer,
        verbose_name=_("Customer"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None)
    role = models.CharField(
        _("Role"),
        max_length=1,
        choices=ROLE_CHOICES,
        blank=False,
        default=ADMIN)
    staff = models.BooleanField(_("Staff Member"), default=False)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_editor(self):
        return self.role == self.EDITOR

    @property
    def is_user(self):
        return self.role == self.USER

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

    def get_absolute_url(self):
        return reverse('users:staff', args=[self.pk])

    def get_form_data(self):
        """
        returns a dictionary that can be used to populate initial data
        """
        return dict(
            role=self.role,
            staff=self.staff,
            customer=self.customer,
            user=self.user,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            email=self.user.email,
        )

    def __str__(self):
        return _("%s's profile") % self.user
