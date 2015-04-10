from django.contrib import admin

from appointments.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Appointment, AppointmentAdmin)
