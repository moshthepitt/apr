from django.contrib import admin

from venues.models import Venue


class VenueAdmin(admin.ModelAdmin):
    pass

admin.site.register(Venue, VenueAdmin)
