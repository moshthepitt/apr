from django.contrib import admin

from appointments.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'client', 'doctor', 'venue', 'event', 'status']
    list_filter = ['customer', 'client', 'status']

admin.site.register(Appointment, AppointmentAdmin)
