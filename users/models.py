from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "%s's profile" % self.user

#### S I G N A L S ####
from . import signals
