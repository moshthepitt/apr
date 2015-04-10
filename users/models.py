from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core import labels


class Client(models.Model):
    """
    This models stores clients in the sense that it is clients who come to any appointments
    """
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    first_name = models.CharField(_('First name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True)
    email = models.EmailField(_('Email address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True, unique=True)
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this client should be treated as '
                                                'active.'))
    creator = models.ForeignKey(User, verbose_name=_("Creator"), on_delete=models.PROTECT)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the client."
        return self.first_name

    def __unicode__(self):
        if self.get_full_name():
            return self.get_full_name()
        return "%s" % self.email

    class Meta:
        verbose_name = getattr(labels, 'CLIENT', _("Client"))
        verbose_name_plural = getattr(labels, 'CLIENT_PLURAL', _("Clients"))


class UserProfile(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return _("%s's profile") % self.user


# ### S I G N A L S ####
from users import signals
