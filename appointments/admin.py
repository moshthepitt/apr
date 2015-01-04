from django.contrib import admin

from .models import Appointment
# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Appointment, AppointmentAdmin)
