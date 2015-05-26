from django.contrib import admin

from appointments.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'client', 'doctor', 'venue', 'event']
    list_filter = ['customer']

admin.site.register(Appointment, AppointmentAdmin)
