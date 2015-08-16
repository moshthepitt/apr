from django.contrib import admin

from appointments.models import Appointment, Tag


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'client', 'doctor', 'venue', 'event', 'status']
    list_filter = ['customer', 'client', 'status']


class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Tag, TagAdmin)
