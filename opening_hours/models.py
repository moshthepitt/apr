import datetime as dt

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from venues.models import Venue
from customers.models import Customer

from core import labels


class OpeningHour(models.Model):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    WEEKDAYS = [
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
        (SATURDAY, _("Saturday")),
        (SUNDAY, _("Sunday")),
    ]

    HOUR_CHOICES = [(x, dt.time(x).strftime('%l %p')) for x in range(24)]

    venue = models.ForeignKey(Venue, verbose_name=getattr(labels, 'VENUE', _("Clinic")))
    customer = models.ForeignKey(Customer, verbose_name=_(
        "Customer"), on_delete=models.PROTECT, default=None, null=True, blank=True)
    weekday = models.IntegerField(_("Weekday"), choices=WEEKDAYS)
    from_hour = models.TimeField(_("Opening Time"), blank=True, null=True)
    to_hour = models.TimeField(_("Closing Time"), blank=True, null=True)

    def clean(self):
        super(OpeningHour, self).clean()
        if None in (self.from_hour, self.to_hour) and (self.from_hour is not None or self.to_hour is not None):
            raise ValidationError(
                _("Both the opening time and closing time must be filled in, or both must be left blank"))

    class Meta:
        verbose_name = getattr(labels, 'OPENING_HOUR', _("Opening Hour"))
        verbose_name_plural = getattr(labels, 'OPENING_HOUR_PLURAL', _("Opening Hours"))
        ordering = ['venue__name', 'weekday', 'from_hour']
        unique_together = ("venue", "weekday")

    def __unicode__(self):
        return "{} {} {} {}".format(self.venue, self.get_weekday_display(), self.from_hour, self.to_hour)

    def get_day_0_6(self):
        """
        returns the day number, where Sun = 0...Sat = 6
        """
        if self.weekday == self.SUNDAY:
            return 0
        return self.weekday

    @property
    def iso_fro(self):
        """ISO from hour"""
        return self.from_hour.isoformat()

    @property
    def iso_to(self):
        """ISO to hour"""
        return self.to_hour.isoformat()

    @property
    def pretty_fro(self):
        """Formatted from hour"""
        return self.from_hour.strftime("%H:%M")

    @property
    def pretty_to(self):
        """Formatted to hour"""
        return self.to_hour.strftime("%H:%M")

    def meta(self):
        return self._meta
