from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return _("%s's profile") % self.user

#### S I G N A L S ####
from . import signals
