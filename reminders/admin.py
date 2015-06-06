from django.contrib import admin

from reminders.models import Reminder


class ReminderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'customer', '_appointment_id',
                    'appointment_time', 'sent_email', 'sent_sms']

admin.site.register(Reminder, ReminderAdmin)
