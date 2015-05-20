from django.contrib import admin

from opening_hours.models import OpeningHour


class OpeningHourAdmin(admin.ModelAdmin):
    pass

admin.site.register(OpeningHour, OpeningHourAdmin)
