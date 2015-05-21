from django.db import models
from django.utils.translation import ugettext_lazy as _

from venues.models import Venue

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

    venue = models.ForeignKey(Venue, verbose_name=getattr(labels, 'VENUE', _("Clinic")))
    weekday = models.IntegerField(_("Weekday"), choices=WEEKDAYS)
    from_hour = models.TimeField(_("From Hour"), )
    to_hour = models.TimeField(_("To Hour"), )

    class Meta:
        verbose_name = getattr(labels, 'OPENING_HOUR', _("Opening Hour"))
        verbose_name_plural = getattr(labels, 'OPENING_HOUR_PLURAL', _("Opening Hours"))
        ordering = ['venue__name', 'weekday', 'from_hour']

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

    def meta(self):
        return self._meta
